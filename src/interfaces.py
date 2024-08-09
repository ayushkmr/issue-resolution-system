"""
interfaces.py

Defines the interfaces for the key components of the system.
"""

from abc import ABC, abstractmethod

class IIssueManager(ABC):
    """
    Interface for managing issues in the system.
    """
    @abstractmethod
    def create_issue(self, transaction_id, issue_type, subject, description, email):
        pass
    
    @abstractmethod
    def get_issue_by_id(self, issue_id):
        pass

    @abstractmethod
    def update_issue(self, issue_id, status, resolution=None):
        pass
    
    @abstractmethod
    def add_to_waitlist(self, issue):
        pass

    @abstractmethod
    def get_next_waiting_issue(self):
        pass

class IAgentManager(ABC):
    """
    Interface for managing agents in the system.
    """
    @abstractmethod
    def add_agent(self, email, name, expertise):
        pass
    
    @abstractmethod
    def get_free_agents(self, issue_type):
        pass
    
    @abstractmethod
    def get_agent_by_id(self, agent_id):
        pass

class IAgent(ABC):
    """
    Interface for a customer service agent in the system.
    """
    @abstractmethod
    def assign_issue(self, issue):
        pass

    @abstractmethod
    def resolve_current_issue(self, resolution):
        pass

class IAgentAssignmentStrategy(ABC):
    """
    Interface for the strategy to assign issues to agents.
    """
    @abstractmethod
    def assign_issue(self, issue):
        pass
    
    @abstractmethod
    def reassign_waiting_issues(self):
        pass
