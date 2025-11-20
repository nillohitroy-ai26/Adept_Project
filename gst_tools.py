from typing import List, Dict, Any
from google.adk.tools import ToolContext
from datetime import datetime


def gst_filing_tool(
    sme_id: str,
    filing_period: str,
    invoices: List[Dict[str, Any]],
    *,  # Force keyword-only from here
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    File GST returns for an SME for a specific period.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        filing_period: The GST filing period in YYYY-MM format (e.g., '2024-01')
        invoices: List of invoice dictionaries, each with invoice_number, amount, and gst_rate
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary containing:
        - result: Success message
        - invoice_count: Number of invoices filed
        - total_value: Total value of all invoices
        - filing_date: Date when filing was completed
    """
    # Calculate total value
    total_value = sum(invoice.get('amount', 0) for invoice in invoices)
    
    # Update compliance status in session state
    if hasattr(tool_context, 'state'):
        if 'compliance_status' not in tool_context.state:
            tool_context.state['compliance_status'] = {}
        
        tool_context.state['compliance_status']['gst_filing'] = {
            'period': filing_period,
            'status': 'filed',
            'invoice_count': len(invoices),
            'total_value': total_value,
            'filing_date': datetime.now().isoformat()
        }
        
        # Add to compliance history
        if 'compliance_history' not in tool_context.state:
            tool_context.state['compliance_history'] = []
        
        tool_context.state['compliance_history'].append({
            'action': 'gst_filing',
            'period': filing_period,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'details': f"Filed GST for {filing_period} with {len(invoices)} invoices, total ₹{total_value:,.2f}"
        })
    
    return {
        'result': f'✅ GST filing for {filing_period} completed successfully',
        'invoice_count': len(invoices),
        'total_value': total_value,
        'filing_date': datetime.now().strftime('%Y-%m-%d')
    }


def invoice_validation_tool(
    sme_id: str,
    invoices: List[Dict[str, Any]],
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Validate invoices for GST compliance.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        invoices: List of invoice dictionaries to validate
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary containing:
        - valid_invoices: Count of valid invoices
        - invalid_invoices: Count of invalid invoices
        - details: Validation summary message
        - issues: List of validation issues found
    """
    valid_count = 0
    invalid_count = 0
    issues = []
    
    for idx, invoice in enumerate(invoices):
        if not invoice.get('invoice_number'):
            invalid_count += 1
            issues.append(f"Invoice {idx + 1}: Missing invoice number")
        elif invoice.get('amount', 0) <= 0:
            invalid_count += 1
            issues.append(f"Invoice {invoice.get('invoice_number')}: Invalid amount")
        elif not invoice.get('gst_rate'):
            invalid_count += 1
            issues.append(f"Invoice {invoice.get('invoice_number')}: Missing GST rate")
        else:
            valid_count += 1
    
    return {
        'valid_invoices': valid_count,
        'invalid_invoices': invalid_count,
        'details': f'Invoice validation complete: {valid_count} valid, {invalid_count} invalid out of {len(invoices)} total',
        'issues': issues
    }


def gst_compliance_check_tool(
    sme_id: str,
    filing_period: str,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Check GST compliance status for a specific period.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        filing_period: The GST filing period in YYYY-MM format (e.g., '2024-01')
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary containing:
        - status: Compliance status (compliant/non-compliant)
        - compliance_issues: Count of compliance issues
        - issues: List of detailed issues
        - recommendations: List of recommended actions
    """
    # Check if filing exists in state
    status = 'compliant'
    issues = []
    recommendations = []
    
    if hasattr(tool_context, 'state'):
        compliance_status = tool_context.state.get('compliance_status', {})
        gst_filing = compliance_status.get('gst_filing', {})
        
        if gst_filing.get('period') != filing_period:
            status = 'non-compliant'
            issues.append({
                'type': 'missing_filing',
                'severity': 'high',
                'description': f'No GST filing found for period {filing_period}'
            })
            recommendations.append(f'• File GST returns for {filing_period} immediately')
    
    if not issues:
        recommendations.append('• All GST filings are up to date')
        recommendations.append('• Continue monitoring compliance status regularly')
    
    return {
        'status': status,
        'compliance_issues': len(issues),
        'issues': issues,
        'recommendations': recommendations
    }
