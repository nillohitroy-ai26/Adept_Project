"""
Tool definitions for Payroll (PF/ESI) compliance operations
"""
from typing import Any, Dict

def payroll_processing_tool(sme_id: str, employee_count: int = 10, salary_month: str = "2024-11", tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for payroll processing with PF/ESI calculations.
    
    Args:
        sme_id: SME identifier
        employee_count: Number of employees
        salary_month: Month for which payroll is processed
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with payroll processing results
    """
    try:
        # Mock salary data
        average_salary = 40000
        total_employees = employee_count if employee_count else 10
        
        # Calculate deductions
        pf_rate = 0.12  # 12% PF
        esi_rate = 0.0475  # 4.75% ESI
        
        total_payroll = average_salary * total_employees
        total_pf_deduction = total_payroll * pf_rate
        total_esi_deduction = total_payroll * esi_rate
        
        result = {
            "action": "payroll_processing",
            "sme_id": sme_id,
            "salary_month": salary_month,
            "employees": total_employees,
            "average_salary": average_salary,
            "total_payroll": total_payroll,
            "total_pf_deduction": round(total_pf_deduction, 2),
            "total_esi_deduction": round(total_esi_deduction, 2),
            "status": "successfully_processed",
            "breakdown": f"✅ Payroll processed for {total_employees} employees in {salary_month}\n   • Total Payroll: ₹{total_payroll:,.2f}\n   • Total PF Deduction (12%): ₹{total_pf_deduction:,.2f}\n   • Total ESI Deduction (4.75%): ₹{total_esi_deduction:,.2f}\n   • Net Payable: ₹{total_payroll - total_pf_deduction - total_esi_deduction:,.2f}"
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["payroll_processing"] = {
                "month": salary_month,
                "employees": total_employees,
                "total_pf": total_pf_deduction,
                "total_esi": total_esi_deduction,
                "status": "processed"
            }
        
        return result
    except Exception as e:
        return {
            "action": "payroll_processing",
            "status": "failed",
            "error": str(e)
        }


def pf_compliance_check_tool(sme_id: str, employee_count: int = 10, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for checking PF compliance.
    
    Args:
        sme_id: SME identifier
        employee_count: Number of employees
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with PF compliance check results
    """
    try:
        # Mock PF compliance - all compliant
        result = {
            "action": "pf_compliance_check",
            "sme_id": sme_id,
            "employees": employee_count if employee_count else 10,
            "compliance_issues": 0,
            "status": "compliant",
            "details": f"✅ All {employee_count if employee_count else 10} employees' PF accounts are in compliance",
            "checks_performed": [
                "✓ PF contribution rate (12%) verified",
                "✓ Employer contribution matched",
                "✓ No late deposits detected",
                "✓ All members within eligibility criteria"
            ]
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["pf_compliance"] = {
                "status": "compliant",
                "employees": employee_count if employee_count else 10,
                "issues": 0
            }
        
        return result
    except Exception as e:
        return {
            "action": "pf_compliance_check",
            "status": "failed",
            "error": str(e)
        }


def esi_compliance_check_tool(sme_id: str, employee_count: int = 10, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for checking ESI compliance.
    
    Args:
        sme_id: SME identifier
        employee_count: Number of employees
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with ESI compliance check results
    """
    try:
        # Mock ESI compliance - all compliant
        result = {
            "action": "esi_compliance_check",
            "sme_id": sme_id,
            "employees": employee_count if employee_count else 10,
            "compliance_issues": 0,
            "status": "compliant",
            "details": f"✅ ESI coverage is compliant for all {employee_count if employee_count else 10} employees",
            "checks_performed": [
                "✓ All eligible employees registered",
                "✓ ESI contributions on time",
                "✓ No outstanding dues",
                "✓ No claim disputes pending"
            ]
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["esi_compliance"] = {
                "status": "compliant",
                "employees": employee_count if employee_count else 10,
                "issues": 0
            }
        
        return result
    except Exception as e:
        return {
            "action": "esi_compliance_check",
            "status": "failed",
            "error": str(e)
        }


def tds_calculation_tool(sme_id: str, payment_type: str = "professional_fees", payment_amount: float = 100000, tool_context=None) -> Dict[str, Any]:
    """
    Mock tool for TDS (Tax Deducted at Source) calculations.
    
    Args:
        sme_id: SME identifier
        payment_type: Type of payment subject to TDS
        payment_amount: Amount of payment
        tool_context: Context from ADK containing session state
    
    Returns:
        Dict with TDS calculation results
    """
    try:
        # Determine TDS rate based on payment type
        tds_rates = {
            "professional_fees": 0.10,  # 10%
            "contract_labor": 0.02,      # 2%
            "commission": 0.10,          # 10%
            "rent": 0.10                 # 10%
        }
        
        tds_rate = tds_rates.get(payment_type, 0.10)
        tds_amount = payment_amount * tds_rate
        
        result = {
            "action": "tds_calculation",
            "sme_id": sme_id,
            "payment_type": payment_type,
            "gross_amount": payment_amount,
            "tds_rate": f"{tds_rate * 100}%",
            "tds_amount": round(tds_amount, 2),
            "net_amount": round(payment_amount - tds_amount, 2),
            "status": "successfully_calculated",
            "summary": f"✅ TDS calculated for {payment_type}\n   • Gross Amount: ₹{payment_amount:,.2f}\n   • TDS Rate: {tds_rate * 100}%\n   • TDS Deduction: ₹{tds_amount:,.2f}\n   • Net Payable: ₹{payment_amount - tds_amount:,.2f}"
        }
        
        if tool_context and hasattr(tool_context, 'state'):
            state = tool_context.state
            if "compliance_status" not in state:
                state["compliance_status"] = {}
            state["compliance_status"]["tds_calculation"] = {
                "payment_type": payment_type,
                "gross_amount": payment_amount,
                "tds_amount": tds_amount,
                "status": "calculated"
            }
        
        return result
    except Exception as e:
        return {
            "action": "tds_calculation",
            "status": "failed",
            "error": str(e)
        }
