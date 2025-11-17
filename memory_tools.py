"""
Memory and preference tools for long-term memory integration
"""
from typing import Any, Dict

def load_sme_preferences_tool(sme_id: str, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for loading SME-specific preferences and patterns.
    
    Args:
        sme_id: SME identifier
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with SME preferences
    """
    try:
        # Mock SME preferences
        preferences = {
            "sme_id": sme_id,
            "filing_frequency": "monthly",
            "risk_tolerance": "low",
            "exception_handling": "proactive",
            "notification_method": "email",
            "preferred_filing_dates": [5, 15, 25],
            "previous_issues": []
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "preferences" in state:
                preferences.update(state["preferences"])
        
        return {
            "action": "load_preferences",
            "sme_id": sme_id,
            "preferences": preferences,
            "status": "preferences_loaded",
            "result": f"SME preferences loaded for {sme_id}"
        }
    except Exception as e:
        return {
            "action": "load_preferences",
            "status": "failed",
            "error": str(e)
        }


def update_compliance_pattern_tool(sme_id: str, pattern_data: dict, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for updating learned compliance patterns.
    
    Args:
        sme_id: SME identifier
        pattern_data: Pattern data to store
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with update confirmation
    """
    try:
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_patterns" not in state:
                state["compliance_patterns"] = []
            
            pattern_record = {
                "pattern_type": pattern_data.get("type", "general"),
                "confidence": pattern_data.get("confidence", 0.0),
                "data": pattern_data
            }
            state["compliance_patterns"].append(pattern_record)
        
        return {
            "action": "update_pattern",
            "sme_id": sme_id,
            "pattern_type": pattern_data.get("type", "general"),
            "status": "pattern_updated",
            "result": f"Compliance pattern updated for {sme_id}"
        }
    except Exception as e:
        return {
            "action": "update_pattern",
            "status": "failed",
            "error": str(e)
        }


def retrieve_compliance_history_tool(sme_id: str, limit: int = 10, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for retrieving compliance history.
    
    Args:
        sme_id: SME identifier
        limit: Maximum number of records to retrieve
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with compliance history
    """
    try:
        history = []
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_history" in state:
                history = state["compliance_history"][-limit:]
        
        return {
            "action": "retrieve_history",
            "sme_id": sme_id,
            "records": len(history),
            "status": "history_retrieved",
            "history": history,
            "result": f"Retrieved {len(history)} compliance history records for {sme_id}"
        }
    except Exception as e:
        return {
            "action": "retrieve_history",
            "status": "failed",
            "error": str(e)
        }


def record_exception_pattern_tool(sme_id: str, exception_data: dict, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for recording exception patterns for proactive detection.
    
    Args:
        sme_id: SME identifier
        exception_data: Exception details
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with exception recording confirmation
    """
    try:
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "exception_log" not in state:
                state["exception_log"] = []
            
            state["exception_log"].append({
                "type": exception_data.get("type", "unknown"),
                "severity": exception_data.get("severity", "medium"),
                "description": exception_data.get("description", ""),
                "timestamp": exception_data.get("timestamp", "")
            })
        
        return {
            "action": "record_exception",
            "sme_id": sme_id,
            "exception_type": exception_data.get("type", "unknown"),
            "severity": exception_data.get("severity", "medium"),
            "status": "exception_recorded",
            "result": f"Exception pattern recorded for {sme_id}"
        }
    except Exception as e:
        return {
            "action": "record_exception",
            "status": "failed",
            "error": str(e)
        }
