"""
Tool definitions for GST compliance operations
"""
from typing import Any, Dict

def gst_filing_tool(sme_id: str, filing_period: str, invoices: list, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for GST filing operations.
    
    Args:
        sme_id: SME identifier
        filing_period: Period for which GST is being filed (e.g., "2024-01")
        invoices: List of invoices for the period
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with filing result and status
    """
    try:
        # Simulate processing invoices
        total_value = sum(inv.get("amount", 5000) for inv in invoices) if invoices else 50 * 5000
        
        result = {
            "action": "gst_filing",
            "sme_id": sme_id,
            "filing_period": filing_period,
            "invoice_count": len(invoices) if invoices else 50,
            "total_value": total_value,
            "status": "successfully_filed",
            "result": f"✅ GST filing for {filing_period} completed with {len(invoices) if invoices else 50} invoices. Total value: ₹{total_value:,.2f}"
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["gst_filing"] = {
                "period": filing_period,
                "status": "filed",
                "invoice_count": len(invoices) if invoices else 50,
                "total_value": total_value
            }
        
        return result
    except Exception as e:
        return {
            "action": "gst_filing",
            "status": "failed",
            "error": str(e)
        }


def invoice_validation_tool(sme_id: str, invoices: list = None, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for validating invoices against GST compliance rules.
    
    Args:
        sme_id: SME identifier
        invoices: List of invoices to validate
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with validation results
    """
    try:
        # Generate sample invoices if not provided
        if invoices is None or len(invoices) == 0:
            invoices = [
                {"invoice_number": f"INV-{i:03d}", "amount": 5000, "gst_rate": 18}
                for i in range(50)
            ]
        
        # Simulate validation: 48 valid, 2 invalid
        valid_count = int(len(invoices) * 0.96)
        invalid_count = len(invoices) - valid_count
        
        result = {
            "action": "invoice_validation",
            "sme_id": sme_id,
            "valid_invoices": valid_count,
            "invalid_invoices": invalid_count,
            "status": "validation_complete",
            "details": f"✓ {valid_count} invoices passed validation | ✗ {invalid_count} invoices have issues",
            "invalid_invoice_details": [
                {"invoice": f"INV-{i:03d}", "issue": "Missing GST number"} for i in range(48, 48 + invalid_count)
            ]
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["invoice_validation"] = {
                "valid_count": valid_count,
                "invalid_count": invalid_count,
                "validation_status": "completed"
            }
        
        return result
    except Exception as e:
        return {
            "action": "invoice_validation",
            "status": "failed",
            "error": str(e)
        }


def gst_compliance_check_tool(sme_id: str, filing_period: str = None, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for checking GST compliance against regulatory rules.
    
    Args:
        sme_id: SME identifier
        filing_period: Filing period to check
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with compliance check results
    """
    try:
        compliance_issues = [
            {
                "type": "late_filing",
                "severity": "high",
                "description": "GST filing was submitted 5 days after deadline. Late fee may apply."
            }
        ]
        
        result = {
            "action": "gst_compliance_check",
            "sme_id": sme_id,
            "filing_period": filing_period or "2024-01",
            "compliance_issues": len(compliance_issues),
            "status": "non_compliant",
            "issues": compliance_issues,
            "recommendations": [
                "⚠️ Apply for late fee waiver with GST authorities",
                "📋 Submit required documentation explaining the delay",
                "📅 Set calendar reminders for next filing due date"
            ]
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "exception_log" not in state:
                state["exception_log"] = []
            state["exception_log"].extend(compliance_issues)
        
        return result
    except Exception as e:
        return {
            "action": "gst_compliance_check",
            "status": "failed",
            "error": str(e)
        }
