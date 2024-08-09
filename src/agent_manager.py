"""
agent_manager.py

Manages the collection of agents and their assignments.
"""

from interfaces import IAgentManager
from agent import Agent, AgentStatus
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AgentManager(IAgentManager):
    """
    Manages the collection of agents and their assignments.
    """
    def __init__(self):
        self.agents = {}

    def add_agent(self, email, name, expertise):
        """
        Adds a new agent to the system with the provided expertise.

        :param email: The email address of the agent
        :param name: The name of the agent
        :param expertise: A list of IssueType instances that the agent is expert in
        :return: The created Agent object
        """
        agent = Agent(email, name, expertise)
        self.agents[agent.agent_id] = agent
        logging.info(f"Agent {name} added to the system with ID {agent.agent_id}")
        return agent

    def get_free_agents(self, issue_type):
        """
        Returns a list of agents who are free and have the required expertise.

        :param issue_type: The type of issue requiring expertise
        :return: A list of free agents with the required expertise
        """
        free_agents = [agent for agent in self.agents.values() if agent.status == AgentStatus.FREE and issue_type in agent.expertise]
        logging.info(f"Found {len(free_agents)} free agents with expertise in {issue_type}")
        return free_agents

    def get_agent_by_id(self, agent_id):
        """
        Retrieves an agent by their ID.

        :param agent_id: The unique ID of the agent
        :return: The Agent object, if found
        """
        return self.agents.get(agent_id)

    def view_agents_work_history(self):
        """
        Returns the work history of all agents.

        :return: A dictionary mapping agent names to their resolved issues
        """
        history = {}
        for agent in self.agents.values():
            history[agent.name] = [issue.issue_id for issue in agent.work_history]
        logging.info("Retrieved agents' work history")
        return history
