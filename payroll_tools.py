from typing import Dict, Any
from google.adk.tools import ToolContext
from datetime import datetime


def payroll_processing_tool(
    sme_id: str,
    employee_count: int,
    salary_month: str,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Process payroll for employees including PF and ESI deductions.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        employee_count: Number of employees to process payroll for
        salary_month: Salary month in YYYY-MM format (e.g., '2024-11')
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary containing payroll breakdown with total amounts and deductions
    """
    # Mock payroll calculation
    avg_salary = 30000
    total_payroll = employee_count * avg_salary
    total_pf_deduction = total_payroll * 0.12  # 12% PF
    total_esi_deduction = total_payroll * 0.0475  # 4.75% ESI
    
    # Update compliance status
    if hasattr(tool_context, 'state'):
        if 'compliance_status' not in tool_context.state:
            tool_context.state['compliance_status'] = {}
        
        tool_context.state['compliance_status']['payroll_processing'] = {
            'month': salary_month,
            'status': 'processed',
            'employee_count': employee_count,
            'total_payroll': total_payroll,
            'processed_date': datetime.now().isoformat()
        }
        
        # Add to compliance history
        if 'compliance_history' not in tool_context.state:
            tool_context.state['compliance_history'] = []
        
        tool_context.state['compliance_history'].append({
            'action': 'payroll_processing',
            'month': salary_month,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'details': f"Processed payroll for {employee_count} employees for {salary_month}, total ₹{total_payroll:,.2f}"
        })
    
    return {
        'result': 'success',
        'employees': employee_count,
        'salary_month': salary_month,
        'total_payroll': total_payroll,
        'total_pf_deduction': total_pf_deduction,
        'total_esi_deduction': total_esi_deduction,
        'breakdown': f"Payroll processed for {employee_count} employees for {salary_month}. Total: ₹{total_payroll:,.2f}, PF: ₹{total_pf_deduction:,.2f}, ESI: ₹{total_esi_deduction:,.2f}"
    }


def pf_compliance_check_tool(
    sme_id: str,
    employee_count: int,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Check Provident Fund (PF) compliance status.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        employee_count: Number of employees
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary with PF compliance status and details
    """
    # Mock compliance check
    status = 'compliant' if employee_count > 0 else 'non-compliant'
    
    return {
        'status': status,
        'employee_count': employee_count,
        'details': f'PF compliance check for {employee_count} employees: {status}'
    }


def esi_compliance_check_tool(
    sme_id: str,
    employee_count: int,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Check Employee State Insurance (ESI) compliance status.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        employee_count: Number of employees
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary with ESI compliance status and details
    """
    # Mock compliance check
    status = 'compliant' if employee_count > 0 else 'non-compliant'
    
    return {
        'status': status,
        'employee_count': employee_count,
        'details': f'ESI compliance check for {employee_count} employees: {status}'
    }


def tds_calculation_tool(
    sme_id: str,
    salary: float,
    *,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Calculate Tax Deducted at Source (TDS) for a given salary.
    
    Args:
        sme_id: The unique identifier of the SME (e.g., 'SME_001')
        salary: Annual salary amount in rupees
        tool_context: Tool execution context (automatically provided by ADK)
    
    Returns:
        Dictionary with TDS calculation breakdown
    """
    # Mock TDS calculation (simplified)
    if salary <= 250000:
        tds_amount = 0
    elif salary <= 500000:
        tds_amount = (salary - 250000) * 0.05
    elif salary <= 1000000:
        tds_amount = 12500 + (salary - 500000) * 0.20
    else:
        tds_amount = 112500 + (salary - 1000000) * 0.30
    
    return {
        'salary': salary,
        'tds_amount': tds_amount,
        'net_salary': salary - tds_amount,
        'details': f'TDS calculated for salary ₹{salary:,.2f}: TDS ₹{tds_amount:,.2f}, Net ₹{salary - tds_amount:,.2f}'
    }
