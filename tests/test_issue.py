import unittest
import sys

try:
    from issue import Issue, IssueStatus
    from issue_type import IssueType
except ImportError:
    sys.path.insert(0, 'src')
    from issue import Issue, IssueStatus
    from issue_type import IssueType

class TestIssue(unittest.TestCase):
    
    def setUp(self):
        self.issue = Issue(
            transaction_id="T1",
            issue_type=IssueType.PAYMENT_RELATED,
            subject="Payment Failed",
            description="Payment failed but money debited",
            email="user@test.com"
        )

    def test_issue_initialization(self):
        self.assertEqual(self.issue.transaction_id, "T1")
        self.assertEqual(self.issue.issue_type, IssueType.PAYMENT_RELATED)
        self.assertEqual(self.issue.subject, "Payment Failed")
        self.assertEqual(self.issue.description, "Payment failed but money debited")
        self.assertEqual(self.issue.email, "user@test.com")
        self.assertEqual(self.issue.status, IssueStatus.OPEN)
        self.assertIsNone(self.issue.resolution)
        self.assertIsNone(self.issue.assigned_agent)

    def test_update_status(self):
        self.issue.update_status(IssueStatus.IN_PROGRESS)
        self.assertEqual(self.issue.status, IssueStatus.IN_PROGRESS)
        self.assertIsNone(self.issue.resolution)

        self.issue.update_status(IssueStatus.RESOLVED, resolution="Refunded")
        self.assertEqual(self.issue.status, IssueStatus.RESOLVED)
        self.assertEqual(self.issue.resolution, "Refunded")

if __name__ == "__main__":
    unittest.main()
