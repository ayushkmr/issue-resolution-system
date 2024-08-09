"""
agent.py

Contains the Agent class which represents a customer service agent, and the AgentStatus enum for tracking agent status.
"""

import uuid
from enum import Enum
from interfaces import IAgent
import logging

from issue import IssueStatus

# Configure logging
logging.basicConfig(level=logging.INFO)

class AgentStatus(Enum):
    """
    Enum representing the possible statuses of an agent.
    """
    FREE = "Free"
    BUSY = "Busy"

class Agent(IAgent):
    """
    Represents a customer service agent.
    """
    def __init__(self, email, name, expertise):
        """
        Initializes an Agent with the given details.

        :param email: The email address of the agent
        :param name: The name of the agent
        :param expertise: A list of IssueType instances that the agent is expert in
        """
        self.agent_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.expertise = expertise  # List of IssueType instances
        self.current_issue = None
        self.work_history = []
        self.status = AgentStatus.FREE
        
        logging.info(f"Agent {self.name} created with expertise in {', '.join(self.expertise)}")

    def assign_issue(self, issue):
        """
        Assigns an issue to the agent if they are free and have the required expertise.

        :param issue: The issue to be assigned
        """
        if self.status == AgentStatus.FREE and issue.issue_type in self.expertise:
            self.current_issue = issue
            self.status = AgentStatus.BUSY
            self.work_history.append(issue)
            issue.assign_to_agent(self)
            logging.info(f"Issue {issue.issue_id} assigned to agent {self.name}")
        else:
            raise Exception(f"Agent {self.name} is not free or lacks expertise")

    def resolve_current_issue(self, resolution):
        """
        Resolves the current issue assigned to the agent.

        :param resolution: Description of how the issue was resolved
        """
        if self.current_issue:
            self.current_issue.update_status(IssueStatus.RESOLVED, resolution)
            self.status = AgentStatus.FREE
            logging.info(f"Agent {self.name} resolved issue {self.current_issue.issue_id}")
            self.current_issue = None
        else:
            raise Exception(f"Agent {self.name} has no current issue to resolve")
