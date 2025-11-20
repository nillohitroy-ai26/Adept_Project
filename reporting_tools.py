from typing import Dict, Any
from google.adk.tools import ToolContext
from datetime import datetime
import uuid


def generate_compliance_report_tool(
    sme_id: str,
    report_type: str,
    period: str,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Generate a compliance report for the specified period.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        report_type: Type of report (quarterly, annual, monthly)
        period: Reporting period (e.g., 'Q1_2024', '2024-01')
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary with report ID, sections, and risk assessment
    """
    report_id = f"RPT-{uuid.uuid4().hex[:8].upper()}"
    
    # Get compliance data from state
    compliance_status = {}
    compliance_history = []
    
    if hasattr(tool_context, 'state'):
        compliance_status = tool_context.state.get('compliance_status', {})
        compliance_history = tool_context.state.get('compliance_history', [])
    
    # Generate report sections
    sections = {
        'Executive_Summary': {
            'total_actions': len(compliance_history),
            'compliance_rate': '95%'
        },
        'GST_Compliance': compliance_status.get('gst_filing', {}),
        'Payroll_Compliance': compliance_status.get('payroll_processing', {}),
        'Risk_Assessment': {
            'overall_risk': 'low',
            'critical_issues': 0,
            'high_priority_issues': 0
        }
    }
    
    return {
        'report_id': report_id,
        'report_type': report_type,
        'period': period,
        'generated_date': datetime.now().strftime('%Y-%m-%d'),
        'sections': sections
    }


def compliance_summary_tool(
    sme_id: str,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Get a summary of current compliance status.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary with compliance snapshot and summary
    """
    compliance_status = {}
    compliance_history = []
    
    if hasattr(tool_context, 'state'):
        compliance_status = tool_context.state.get('compliance_status', {})
        compliance_history = tool_context.state.get('compliance_history', [])
    
    # Build summary
    summary_lines = ["📊 Compliance Summary for " + sme_id, "=" * 50]
    
    if compliance_status:
        summary_lines.append("\n✅ Active Compliance Items:")
        for key, value in compliance_status.items():
            summary_lines.append(f"  • {key.replace('_', ' ').title()}: {value.get('status', 'unknown')}")
    else:
        summary_lines.append("\n⚠️ No compliance actions recorded yet")
    
    if compliance_history:
        summary_lines.append(f"\n📋 Recent Actions ({len(compliance_history)}):")
        for item in compliance_history[-3:]:  # Last 3 items
            summary_lines.append(f"  • {item.get('action', 'unknown')}: {item.get('status', 'unknown')}")
    
    snapshot = "\n".join(summary_lines)
    
    return {
        'compliance_snapshot': snapshot,
        'total_items': len(compliance_status),
        'recent_actions': len(compliance_history)
    }


def audit_trail_retrieval_tool(
    sme_id: str,
    start_date: str,
    end_date: str,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Retrieve audit trail for a date range.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary with audit trail entries for the specified period
    """
    compliance_history = []
    
    if hasattr(tool_context, 'state'):
        compliance_history = tool_context.state.get('compliance_history', [])
    
    # Filter by date range (simplified)
    filtered_history = compliance_history  # In real implementation, filter by dates
    
    return {
        'audit_trail': filtered_history,
        'start_date': start_date,
        'end_date': end_date,
        'total_entries': len(filtered_history)
    }
