"""
issue_type.py

Defines the different types of issues that can be handled by the system.
"""

class IssueType:
    """
    Represents the types of issues that can be raised by customers.
    """
    PAYMENT_RELATED = "Payment Related"
    MUTUAL_FUND_RELATED = "Mutual Fund Related"
    GOLD_RELATED = "Gold Related"
    INSURANCE_RELATED = "Insurance Related"
    
    @classmethod
    def all_types(cls):
        """
        Returns a list of all possible issue types.
        """
        return [cls.PAYMENT_RELATED, cls.MUTUAL_FUND_RELATED, cls.GOLD_RELATED, cls.INSURANCE_RELATED]
