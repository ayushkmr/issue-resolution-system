"""
main.py

Simulates the workflow of the Customer Issue Resolution System using multithreading.
"""

import sys
import threading
import time
import json
from issue import IssueStatus
from issue_manager import IssueManager
from agent_manager import AgentManager
from agent_assignment_strategy import AgentAssignmentStrategy
from issue_type import IssueType
from factory import IssueFactory, AgentFactory, UserFactory

# Global lock for synchronizing access to shared resources
lock = threading.Lock()

def load_initial_data(agent_manager, user_factory):
    """
    Loads initial agents and users from a JSON file.

    :param agent_manager: The AgentManager instance
    :param user_factory: The UserFactory instance
    :return: A list of User objects
    """
    with open('src/initial_data.json', 'r') as file:
        data = json.load(file)

    for agent_data in data['agents']:
        agent_manager.add_agent(agent_data['email'], agent_data['name'], agent_data['expertise'])

    users = []
    for user_data in data['users']:
        user = user_factory.create_user(user_data['email'], user_data['name'])
        users.append(user)

    return users

def create_issues(user, issue_manager):
    """
    Function to create issues in a separate thread.

    :param user: The User object raising the issue
    :param issue_manager: The IssueManager instance
    """
    with lock:
        issue1 = user.raise_issue(issue_manager, "T1", IssueType.PAYMENT_RELATED, "Payment Failed", "My payment failed but money is debited")
        time.sleep(2)  # Simulating delay in raising the next issue
        issue2 = user.raise_issue(issue_manager, "T2", IssueType.MUTUAL_FUND_RELATED, "Purchase Failed", "Unable to purchase Mutual Fund")
        time.sleep(2)  # Simulating delay in raising the next issue
        issue3 = user.raise_issue(issue_manager, "T3", IssueType.PAYMENT_RELATED, "Payment Failed", "My payment failed but money is debited")
    return [issue1, issue2, issue3]

def assign_issues(strategy, issues, issue_manager):
    """
    Function to assign issues in a separate thread.

    :param strategy: The AgentAssignmentStrategy instance
    :param issues: List of issues to be assigned
    :param issue_manager: The IssueManager instance
    """
    with lock:
        for issue in issues:
            issue_manager.try_assign_issue(strategy, issue)
            time.sleep(3)  # Simulating delay in assigning issues

def resolve_issues(agent, issue_manager):
    """
    Function to resolve issues in a separate thread.

    :param agent: The Agent object resolving issues
    :param issue_manager: The IssueManager instance
    """
    with lock:
        if agent.current_issue:
            issue_manager.update_issue(agent.current_issue.issue_id, IssueStatus.RESOLVED)
            agent.resolve_current_issue("Issue resolved by refunding the amount")
            time.sleep(5)  # Simulating delay in resolving the issue

def reassign_waiting_issues(strategy, issue_manager):
    """
    Function to periodically reassign waiting issues in a separate thread.

    :param strategy: The AgentAssignmentStrategy instance
    :param issue_manager: The IssueManager instance
    """
    while True:
        with lock:
            waiting_issues = issue_manager.get_issues_by_status(IssueStatus.WAITING)
            for issue in waiting_issues:
                issue_manager.try_assign_issue(strategy, issue)
            time.sleep(10)  # Check and reassign every 10 seconds

def main():
    # Initialize managers
    issue_manager = IssueManager()
    agent_manager = AgentManager()
    strategy = AgentAssignmentStrategy(agent_manager, issue_manager)

    # Load initial data
    users = load_initial_data(agent_manager, UserFactory)

    # Run the simulation in separate threads
    issue_thread = threading.Thread(target=create_issues, args=(users[0], issue_manager))
    issue_thread.start()
    issue_thread.join()  # Wait for issue creation to complete before assignment starts

    assign_thread = threading.Thread(target=assign_issues, args=(strategy, list(issue_manager.issues.values()), issue_manager))
    assign_thread.start()
    assign_thread.join()  # Wait for assignment to complete before resolution starts

    # Resolve issues for each agent
    resolve_threads = []
    for agent in agent_manager.agents.values():
        resolve_thread = threading.Thread(target=resolve_issues, args=(agent, issue_manager))
        resolve_threads.append(resolve_thread)
        resolve_thread.start()

    for thread in resolve_threads:
        thread.join()

    # Start reassigning waiting issues in the background
    reassign_thread = threading.Thread(target=reassign_waiting_issues, args=(strategy, issue_manager))
    reassign_thread.start()

    # Print agent work history
    for agent in agent_manager.agents.values():
        print(f"Agent {agent.name} worked on: {[issue.issue_id for issue in agent.work_history]}")

    # Print issues by status
    for status in [IssueStatus.OPEN, IssueStatus.IN_PROGRESS, IssueStatus.RESOLVED, IssueStatus.WAITING]:
        print(f"Issues with status {status.value}: {[issue.issue_id for issue in issue_manager.get_issues_by_status(status)]}")

    # Exit the program gracefully
    sys.exit(0)

if __name__ == "__main__":
    main()
