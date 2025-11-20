"""
Conversation Context Manager for Problem 2 Fix

This module tracks conversation state to recognize when user is providing
follow-up information (like "50" after being asked for invoice count).
"""
from typing import Optional, Dict, Any
from datetime import datetime


class ConversationContext:
    """
    Tracks conversation state for multi-turn interactions.
    Enables agent to recognize follow-up responses.
    """
    
    def __init__(self):
        self.waiting_for_input = False
        self.expected_input_type = None
        self.pending_action = None
        self.pending_params = {}
        self.last_query = None
        self.last_query_time = None
    
    def is_waiting(self) -> bool:
        """Check if agent is waiting for follow-up input."""
        return self.waiting_for_input
    
    def set_waiting(
        self,
        input_type: str,
        action: str,
        params: Dict[str, Any],
        last_query: str
    ):
        """
        Set agent to waiting state for user input.
        
        Args:
            input_type: Type of input expected (e.g., 'invoice_count', 'employee_count')
            action: Pending action name (e.g., 'gst_filing', 'payroll_processing')
            params: Parameters already collected
            last_query: The original query that triggered this
        """
        self.waiting_for_input = True
        self.expected_input_type = input_type
        self.pending_action = action
        self.pending_params = params.copy()
        self.last_query = last_query
        self.last_query_time = datetime.now()
    
    def get_pending(self) -> tuple:
        """
        Get pending action and clear waiting state.
        
        Returns:
            Tuple of (action, params, last_query)
        """
        action = self.pending_action
        params = self.pending_params.copy()
        last_query = self.last_query
        self.clear()
        return action, params, last_query
    
    def clear(self):
        """Clear waiting state."""
        self.waiting_for_input = False
        self.expected_input_type = None
        self.pending_action = None
        self.pending_params = {}
        self.last_query = None
        self.last_query_time = None
    
    def get_context_info(self) -> Dict[str, Any]:
        """Get current context information for debugging."""
        return {
            'waiting': self.waiting_for_input,
            'expected_type': self.expected_input_type,
            'pending_action': self.pending_action,
            'last_query': self.last_query
        }


def is_follow_up_response(user_input: str, context: ConversationContext) -> bool:
    """
    Determine if user input is a follow-up response to a previous question.
    
    This prevents the agent from rejecting simple numeric or short responses
    when it's waiting for additional information.
    
    Args:
        user_input: User's current input
        context: Conversation context
    
    Returns:
        True if this is likely a follow-up response
    """
    if not context.is_waiting():
        return False
    
    user_input_stripped = user_input.strip().lower()
    
    # Check if it's a numeric response when expecting count
    if context.expected_input_type in ['invoice_count', 'employee_count', 'count']:
        # Just a number or "N invoices/employees"
        import re
        if re.match(r'^\d+(\s+(invoice|invoices|employee|employees))?$', user_input_stripped):
            return True
    
    # Check if it's a date/period response when expecting period
    if context.expected_input_type in ['period', 'month', 'filing_period']:
        # Month name, date format, or period
        month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                      'july', 'august', 'september', 'october', 'november', 'december']
        if any(month in user_input_stripped for month in month_names):
            return True
        if re.match(r'^\d{4}-\d{2}$', user_input_stripped):
            return True
        if re.match(r'^q[1-4]\s+\d{4}$', user_input_stripped):
            return True
    
    return False


def parse_follow_up_input(
    user_input: str,
    expected_type: str
) -> Optional[Any]:
    """
    Parse follow-up input based on expected type.
    
    Args:
        user_input: User's input
        expected_type: Type of input expected
    
    Returns:
        Parsed value or None if parsing failed
    """
    import re
    
    user_input_stripped = user_input.strip().lower()
    
    # Parse numeric count
    if expected_type in ['invoice_count', 'employee_count', 'count']:
        match = re.search(r'(\d+)', user_input_stripped)
        if match:
            return int(match.group(1))
    
    # Parse period
    if expected_type in ['period', 'month', 'filing_period']:
        # Try month + year
        month_match = re.search(
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
            user_input_stripped
        )
        if month_match:
            months = ['january', 'february', 'march', 'april', 'may', 'june',
                     'july', 'august', 'september', 'october', 'november', 'december']
            month_name = month_match.group(1)
            year = month_match.group(2)
            month_num = months.index(month_name) + 1
            return f"{year}-{month_num:02d}"
        
        # Try YYYY-MM format
        if re.match(r'^\d{4}-\d{2}$', user_input_stripped):
            return user_input_stripped
        
        # Try Q format
        quarter_match = re.match(r'^q([1-4])\s+(\d{4})$', user_input_stripped)
        if quarter_match:
            return f"Q{quarter_match.group(1)}_{quarter_match.group(2)}"
    
    return None
