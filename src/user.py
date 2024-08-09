"""
user.py

Contains the User class which represents a customer who can raise issues in the system.
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class User:
    """
    Represents a user in the system.
    """
    def __init__(self, email, name):
        """
        Initializes a User with the given details.

        :param email: The email address of the user
        :param name: The name of the user
        """
        self.email = email
        self.name = name
        logging.info(f"User created: {self.name} with email {self.email}")

    def raise_issue(self, issue_manager, transaction_id, issue_type, subject, description):
        """
        Raises an issue in the system.

        :param issue_manager: The IssueManager instance
        :param transaction_id: ID of the transaction related to the issue
        :param issue_type: Type of the issue
        :param subject: Subject of the issue
        :param description: Detailed description of the issue
        :return: The created Issue object
        """
        issue = issue_manager.create_issue(transaction_id, issue_type, subject, description, self.email)
        logging.info(f"{self.name} raised issue {issue.issue_id} with subject '{subject}'")
        return issue
