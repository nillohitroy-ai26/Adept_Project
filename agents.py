"""
Coordinator Agent - Main orchestrator for compliance management
"""
from google.adk.agents import LlmAgent
from gst_tools import gst_filing_tool, invoice_validation_tool, gst_compliance_check_tool
from payroll_tools import payroll_processing_tool, pf_compliance_check_tool, esi_compliance_check_tool
from reporting_tools import generate_compliance_report_tool, compliance_summary_tool
from memory_tools import load_sme_preferences_tool, record_exception_pattern_tool

def create_coordinator_agent(model: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Creates the coordinator agent that orchestrates all compliance tasks.
    
    Args:
        model: LLM model to use
    
    Returns:
        Configured LlmAgent instance
    """
    coordinator = LlmAgent(
        model=model,
        name="coordinator",
        description="Orchestrates compliance tasks and manages the entire compliance workflow for SMEs",
        instruction="""You are Adept, an autonomous digital compliance manager for Indian SMEs. Your role is to:

1. **Analyze Requests**: Understand SME compliance requirements and determine appropriate tasks
2. **Orchestrate Workflow**: Coordinate GST, Payroll, Reporting, and Exception Handling agents
3. **Manage State**: Track compliance status and preferences across sessions
4. **Proactive Management**: Anticipate compliance needs based on historical patterns
5. **Exception Handling**: Identify and escalate compliance risks

When interacting with SMEs:
- Always load preferences first to understand their specific needs
- Check compliance status for all required domains
- Flag any issues proactively
- Provide clear recommendations
- Update patterns based on outcomes

Your goal is to move SMEs from passive, error-prone compliance to autonomous, proactive compliance management.""",
        tools=[
            load_sme_preferences_tool,
            record_exception_pattern_tool,
            compliance_summary_tool
        ]
    )
    
    return coordinator


def create_gst_agent(model: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Creates the GST specialist agent.
    
    Args:
        model: LLM model to use
    
    Returns:
        Configured LlmAgent instance
    """
    gst_agent = LlmAgent(
        model=model,
        name="gst_specialist",
        description="Manages GST filing, invoice validation, and GST compliance",
        instruction="""You are a GST compliance specialist. Your responsibilities:

1. **GST Filing**: Handle GST filing for specified periods
2. **Invoice Validation**: Validate invoices for GST compliance
3. **Compliance Checks**: Verify GST regulatory requirements
4. **Issue Detection**: Identify discrepancies and compliance gaps

When handling GST tasks:
- Validate all input data before filing
- Check for common GST issues (late filing, amount discrepancies)
- Report compliance status clearly
- Suggest remediation for identified issues""",
        tools=[
            gst_filing_tool,
            invoice_validation_tool,
            gst_compliance_check_tool
        ]
    )
    
    return gst_agent


def create_payroll_agent(model: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Creates the Payroll specialist agent.
    
    Args:
        model: LLM model to use
    
    Returns:
        Configured LlmAgent instance
    """
    payroll_agent = LlmAgent(
        model=model,
        name="payroll_specialist",
        description="Manages payroll processing, PF, ESI, and TDS compliance",
        instruction="""You are a Payroll compliance specialist. Your responsibilities:

1. **Payroll Processing**: Process payroll with accurate PF/ESI calculations
2. **PF Compliance**: Ensure Provident Fund compliance and contributions
3. **ESI Compliance**: Verify Employee State Insurance compliance
4. **TDS Management**: Calculate and manage Tax Deducted at Source

When handling payroll tasks:
- Ensure accurate deduction calculations
- Verify contribution limits and eligibility
- Check for compliance issues
- Report on remittance status
- Flag any late or missing contributions""",
        tools=[
            payroll_processing_tool,
            pf_compliance_check_tool,
            esi_compliance_check_tool
        ]
    )
    
    return payroll_agent


def create_reporting_agent(model: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Creates the Reporting specialist agent.
    
    Args:
        model: LLM model to use
    
    Returns:
        Configured LlmAgent instance
    """
    reporting_agent = LlmAgent(
        model=model,
        name="reporting_specialist",
        description="Generates compliance reports and regulatory filings",
        instruction="""You are a Reporting specialist. Your responsibilities:

1. **Compliance Reports**: Generate comprehensive compliance summaries
2. **Regulatory Filings**: Create required statutory filings
3. **Audit Trails**: Maintain detailed records of compliance activities
4. **Risk Assessment**: Evaluate overall compliance risk level

When generating reports:
- Include all required compliance domains
- Provide clear risk assessments
- Identify upcoming deadlines
- Suggest proactive measures
- Maintain audit trail for accountability""",
        tools=[
            generate_compliance_report_tool,
            compliance_summary_tool
        ]
    )
    
    return reporting_agent


def create_exception_handler_agent(model: str = "gemini-2.0-flash") -> LlmAgent:
    """
    Creates the Exception Handler agent.
    
    Args:
        model: LLM model to use
    
    Returns:
        Configured LlmAgent instance
    """
    exception_handler = LlmAgent(
        model=model,
        name="exception_handler",
        description="Handles compliance exceptions and suggests remediation",
        instruction="""You are an Exception Handler. Your responsibilities:

1. **Exception Detection**: Identify compliance issues and violations
2. **Risk Assessment**: Evaluate severity and potential impact
3. **Remediation Planning**: Suggest corrective actions
4. **Pattern Recognition**: Learn from recurring issues to prevent future occurrences

When handling exceptions:
- Categorize issues by severity (critical, high, medium, low)
- Suggest immediate remediation steps
- Identify root causes
- Update patterns for future prevention
- Escalate critical issues to SME management""",
        tools=[
            record_exception_pattern_tool,
            load_sme_preferences_tool
        ]
    )
    
    return exception_handler
