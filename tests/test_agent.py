import unittest
import sys

try:
    from agent import Agent, AgentStatus
    from issue import Issue
    from issue_type import IssueType
except ImportError:
    sys.path.insert(0, 'src')
    from agent import Agent, AgentStatus
    from issue import Issue
    from issue_type import IssueType

class TestAgent(unittest.TestCase):
    
    def setUp(self):
        self.agent = Agent(email="agent@test.com", name="Test Agent", expertise=[IssueType.PAYMENT_RELATED])

    def test_agent_initialization(self):
        self.assertEqual(self.agent.email, "agent@test.com")
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.expertise, [IssueType.PAYMENT_RELATED])
        self.assertEqual(self.agent.status, AgentStatus.FREE)
        self.assertIsNone(self.agent.current_issue)
        self.assertEqual(self.agent.work_history, [])

    def test_assign_issue(self):
        issue = Issue(transaction_id="T1", issue_type=IssueType.PAYMENT_RELATED, subject="Payment Failed", description="Payment failed", email="user@test.com")
        self.agent.assign_issue(issue)
        self.assertEqual(self.agent.current_issue, issue)
        self.assertEqual(self.agent.status, AgentStatus.BUSY)

    def test_resolve_issue(self):
        issue = Issue(transaction_id="T1", issue_type=IssueType.PAYMENT_RELATED, subject="Payment Failed", description="Payment failed", email="user@test.com")
        self.agent.assign_issue(issue)
        self.agent.resolve_current_issue(resolution="Refunded")
        
        self.assertIsNone(self.agent.current_issue)
        self.assertEqual(self.agent.status, AgentStatus.FREE)
        self.assertIn(issue, self.agent.work_history)
        self.assertEqual(issue.resolution, "Refunded")

if __name__ == "__main__":
    unittest.main()
