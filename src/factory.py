"""
factory.py

Provides factory classes for creating instances of Issue, Agent, and User.
"""

from issue import Issue
from agent import Agent
from user import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class IssueFactory:
    """
    Factory for creating Issue instances.
    """
    @staticmethod
    def create_issue(transaction_id, issue_type, subject, description, email):
        """
        Creates and returns a new Issue instance.

        :param transaction_id: ID of the transaction related to the issue
        :param issue_type: Type of the issue
        :param subject: Subject of the issue
        :param description: Detailed description of the issue
        :param email: Email of the user who raised the issue
        :return: The created Issue object
        """
        issue = Issue(transaction_id, issue_type, subject, description, email)
        logging.info(f"Issue created with transaction ID {transaction_id}")
        return issue

class AgentFactory:
    """
    Factory for creating Agent instances.
    """
    @staticmethod
    def create_agent(email, name, expertise):
        """
        Creates and returns a new Agent instance.

        :param email: The email address of the agent
        :param name: The name of the agent
        :param expertise: A list of IssueType instances that the agent is expert in
        :return: The created Agent object
        """
        agent = Agent(email, name, expertise)
        logging.info(f"Agent created with email {email}")
        return agent

class UserFactory:
    """
    Factory for creating User instances.
    """
    @staticmethod
    def create_user(email, name):
        """
        Creates and returns a new User instance.

        :param email: The email address of the user
        :param name: The name of the user
        :return: The created User object
        """
        user = User(email, name)
        logging.info(f"User created with email {email}")
        return user
