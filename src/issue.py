"""
issue.py

Contains the Issue class which represents a customer issue, and the IssueStatus enum for tracking issue status.
"""

import uuid
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)

class IssueStatus(Enum):
    """
    Enum representing the possible statuses of an issue.
    """
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    WAITING = "Waiting"

class Issue:
    """
    Represents a customer issue.
    """
    def __init__(self, transaction_id, issue_type, subject, description, email):
        """
        Initializes an Issue with the given details.

        :param transaction_id: ID of the transaction related to the issue
        :param issue_type: Type of the issue
        :param subject: Subject of the issue
        :param description: Detailed description of the issue
        :param email: Email of the user who raised the issue
        """
        self.issue_id = str(uuid.uuid4())
        self.transaction_id = transaction_id
        self.issue_type = issue_type
        self.subject = subject
        self.description = description
        self.email = email
        self.status = IssueStatus.OPEN
        self.resolution = None
        self.assigned_agent = None
        
        logging.info(f"Issue {self.issue_id} created by {email} with type {self.issue_type}")

    def update_status(self, status, resolution=None):
        """
        Updates the status of the issue and optionally sets a resolution.

        :param status: The new status of the issue (IssueStatus enum)
        :param resolution: Optional resolution description
        """
        if self.status != status:  # Only update if the status is changed
            self.status = status
            if resolution:
                self.resolution = resolution
            logging.info(f"Issue {self.issue_id} status updated to {self.status.value}")

    def assign_to_agent(self, agent):
        """
        Assigns the issue to a specific agent.

        :param agent: The agent to whom the issue is assigned
        """
        self.assigned_agent = agent
        logging.info(f"Issue {self.issue_id} assigned to agent {agent.name}")
