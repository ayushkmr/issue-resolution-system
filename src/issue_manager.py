"""
issue_manager.py

Manages the collection of issues and their assignments, including retry logic for issue assignment.
"""

from collections import deque, defaultdict
from interfaces import IIssueManager
from issue import Issue, IssueStatus
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class IssueManager(IIssueManager):
    """
    Manages the collection of issues and their assignments.
    """
    MAX_RETRY_COUNT = 5  # Maximum retries for assigning an issue

    def __init__(self):
        self.issues = {}
        self.waiting_issues = deque()
        self.retry_count = defaultdict(int)
        self.issues_by_status = {
            IssueStatus.OPEN: [],
            IssueStatus.IN_PROGRESS: [],
            IssueStatus.RESOLVED: [],
            IssueStatus.WAITING: []
        }

    def create_issue(self, transaction_id, issue_type, subject, description, email):
        """
        Creates a new issue and adds it to the issue list.

        :param transaction_id: ID of the transaction related to the issue
        :param issue_type: Type of the issue
        :param subject: Subject of the issue
        :param description: Detailed description of the issue
        :param email: Email of the user who raised the issue
        :return: The created Issue object
        """
        issue = Issue(transaction_id, issue_type, subject, description, email)
        self.issues[issue.issue_id] = issue
        self.issues_by_status[IssueStatus.OPEN].append(issue)
        logging.info(f"Issue {issue.issue_id} created and added to the system")
        return issue

    def get_issue_by_id(self, issue_id):
        """
        Retrieves an issue by its ID.

        :param issue_id: The unique ID of the issue
        :return: The Issue object, if found
        """
        return self.issues.get(issue_id)

    def get_issues(self, filter):
        """
        Retrieves issues based on a provided filter.

        :param filter: A dictionary containing filter criteria (e.g., status, email)
        :return: A list of issues that match the filter criteria
        """
        filtered_issues = []
        for issue in self.issues.values():
            match = True
            for key, value in filter.items():
                if getattr(issue, key) != value:
                    match = False
                    break
            if match:
                filtered_issues.append(issue)
        logging.info(f"Filtered issues based on criteria: {filter}")
        return filtered_issues

    def update_issue(self, issue_id, status, resolution=None):
        """
        Updates the status of an issue and optionally sets a resolution.

        :param issue_id: The unique ID of the issue
        :param status: The new status of the issue (IssueStatus enum)
        :param resolution: Optional resolution description
        """
        issue = self.get_issue_by_id(issue_id)
        if issue:
            # Update status tracking
            old_status = issue.status
            issue.update_status(status, resolution)
            self.issues_by_status[old_status].remove(issue)
            self.issues_by_status[status].append(issue)

            logging.info(f"Issue {issue_id} updated with status {status.value}")

    def add_to_waitlist(self, issue):
        """
        Adds an issue to the waitlist for later assignment and changes its status to WAITING.

        :param issue: The Issue object to be waitlisted
        """
        issue.update_status(IssueStatus.WAITING)
        self.waiting_issues.append(issue)
        logging.info(f"Issue {issue.issue_id} added to waitlist with status {IssueStatus.WAITING.value}")

    def get_next_waiting_issue(self):
        """
        Retrieves the next issue from the waitlist for assignment.

        :return: The next Issue object in the waitlist, if available
        """
        if self.waiting_issues:
            issue = self.waiting_issues.popleft()
            logging.info(f"Issue {issue.issue_id} retrieved from waitlist for assignment")
            return issue
        else:
            logging.info("No issues in waitlist")
            return None

    def try_assign_issue(self, strategy, issue):
        """
        Attempts to assign an issue to an agent with retry logic.

        :param strategy: The AgentAssignmentStrategy instance
        :param issue: The Issue object to be assigned
        """
        try:
            strategy.assign_issue(issue)
        except Exception as e:
            self.retry_count[issue.issue_id] += 1
            logging.warning(f"Failed to assign issue {issue.issue_id}: {e}")
            if self.retry_count[issue.issue_id] < self.MAX_RETRY_COUNT:
                logging.info(f"Retrying assignment for issue {issue.issue_id} (Attempt {self.retry_count[issue.issue_id]})")
                self.try_assign_issue(strategy, issue)
            else:
                logging.error(f"Max retries reached for issue {issue.issue_id}. Adding to waiting status.")
                self.add_to_waitlist(issue)

    def get_issues_by_status(self, status):
        """
        Retrieves the list of issues by their status.

        :param status: The IssueStatus enum
        :return: A list of Issue objects with the specified status
        """
        return self.issues_by_status[status]


    def resolve_issue(self, issue_id, resolution):
        """
        Resolves an issue by its ID with the provided resolution.

        :param issue_id: The ID of the issue to be resolved
        :param resolution: Description of how the issue was resolved
        """
        issue = self.issues.get(issue_id)
        if issue:
            issue.update_status(IssueStatus.RESOLVED, resolution)
            logging.info(f"Issue {issue_id} resolved with resolution: {resolution}")
        else:
            logging.error(f"Issue {issue_id} not found for resolution")
