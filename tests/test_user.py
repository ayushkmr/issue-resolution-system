import unittest
import sys

try:
    from user import User
    from issue_manager import IssueManager
    from issue_type import IssueType
except ImportError:
    sys.path.insert(0, 'src')
    from user import User
    from issue_manager import IssueManager
    from issue_type import IssueType

class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.user = User(email="testuser@test.com", name="Test User")
        self.issue_manager = IssueManager()

    def test_raise_issue(self):
        issue = self.user.raise_issue(
            self.issue_manager,
            transaction_id="T1",
            issue_type=IssueType.PAYMENT_RELATED,
            subject="Payment Failed",
            description="Payment failed but money debited"
        )
        
        self.assertEqual(issue.transaction_id, "T1")
        self.assertEqual(issue.issue_type, IssueType.PAYMENT_RELATED)
        self.assertEqual(issue.subject, "Payment Failed")
        self.assertEqual(issue.description, "Payment failed but money debited")
        self.assertEqual(issue.email, "testuser@test.com")

    def test_raise_multiple_issues(self):
        issue1 = self.user.raise_issue(
            self.issue_manager,
            transaction_id="T1",
            issue_type=IssueType.PAYMENT_RELATED,
            subject="Payment Failed",
            description="Payment failed but money debited"
        )
        issue2 = self.user.raise_issue(
            self.issue_manager,
            transaction_id="T2",
            issue_type=IssueType.GOLD_RELATED,
            subject="Gold Purchase Failed",
            description="Unable to purchase gold"
        )
        
        self.assertNotEqual(issue1.issue_id, issue2.issue_id)
        self.assertEqual(len(self.issue_manager.issues), 2)

if __name__ == "__main__":
    unittest.main()
