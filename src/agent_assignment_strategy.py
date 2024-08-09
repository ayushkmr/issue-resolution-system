"""
agent_assignment_strategy.py

Implements the strategy for assigning issues to agents based on their availability and expertise.
"""

from interfaces import IAgentAssignmentStrategy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AgentAssignmentStrategy(IAgentAssignmentStrategy):
    """
    Strategy for assigning issues to agents based on their availability and expertise.
    """
    def __init__(self, agent_manager, issue_manager):
        """
        Initializes the assignment strategy with the necessary managers.

        :param agent_manager: The AgentManager instance
        :param issue_manager: The IssueManager instance
        """
        self.agent_manager = agent_manager
        self.issue_manager = issue_manager

    def assign_issue(self, issue):
        """
        Assigns an issue to a free agent with the appropriate expertise. If no agent is available, the issue is waitlisted.

        :param issue: The Issue object to be assigned
        """
        free_agents = self.agent_manager.get_free_agents(issue.issue_type)
        if free_agents:
            # Sort agents by the number of issues they've resolved (least first)
            free_agents.sort(key=lambda agent: len(agent.work_history))
            agent = free_agents[0]
            agent.assign_issue(issue)
            logging.info(f"Issue {issue.issue_id} assigned to agent {agent.name}")
        else:
            self.issue_manager.add_to_waitlist(issue)
            logging.info(f"No free agents available; Issue {issue.issue_id} added to waitlist")

    def reassign_waiting_issues(self):
        """
        Attempts to reassign issues from the waitlist to free agents.
        """
        issue = self.issue_manager.get_next_waiting_issue()
        while issue:
            self.assign_issue(issue)
            issue = self.issue_manager.get_next_waiting_issue()
