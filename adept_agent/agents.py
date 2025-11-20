"""
Adept Compliance Agent for ADK Web
Complete working version with all tools and proper configuration
"""
from google.adk.agents import LlmAgent
from gst_tools import gst_filing_tool, invoice_validation_tool, gst_compliance_check_tool
from payroll_tools import payroll_processing_tool, pf_compliance_check_tool, esi_compliance_check_tool
from reporting_tools import generate_compliance_report_tool, compliance_summary_tool
from memory_tools import load_sme_preferences_tool, record_exception_pattern_tool
from dotenv import load_dotenv
import os
import sys

from google.adk.agents import LlmAgent
from dotenv import load_dotenv
import os
import sys

# Configure paths for tool imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Get configuration
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL", "gemini-2.0-flash")

print(f"\n{'='*60}")
print("🚀 Initializing Adept Compliance Agent for ADK Web")
print(f"{'='*60}")
print(f"Model: {model}")
print(f"API Key configured: {'✓' if api_key else '✗'}")

# Import all tools
tools_list = []
import_errors = []

# GST Tools
try:
    from gst_tools import (
        gst_filing_tool,
        invoice_validation_tool,
        gst_compliance_check_tool
    )
    tools_list.extend([
        gst_filing_tool,
        invoice_validation_tool,
        gst_compliance_check_tool
    ])
    print("✓ GST tools imported successfully (3 tools)")
except Exception as e:
    import_errors.append(f"GST tools: {str(e)}")
    print(f"✗ GST tools import failed: {e}")

# Payroll Tools
try:
    from payroll_tools import (
        payroll_processing_tool,
        pf_compliance_check_tool,
        esi_compliance_check_tool,
        tds_calculation_tool
    )
    tools_list.extend([
        payroll_processing_tool,
        pf_compliance_check_tool,
        esi_compliance_check_tool,
        tds_calculation_tool
    ])
    print("✓ Payroll tools imported successfully (4 tools)")
except Exception as e:
    import_errors.append(f"Payroll tools: {str(e)}")
    print(f"✗ Payroll tools import failed: {e}")

# Reporting Tools
try:
    from reporting_tools import (
        generate_compliance_report_tool,
        compliance_summary_tool,
        audit_trail_retrieval_tool
    )
    tools_list.extend([
        generate_compliance_report_tool,
        compliance_summary_tool,
        audit_trail_retrieval_tool
    ])
    print("✓ Reporting tools imported successfully (3 tools)")
except Exception as e:
    import_errors.append(f"Reporting tools: {str(e)}")
    print(f"✗ Reporting tools import failed: {e}")

print(f"\nTotal tools loaded: {len(tools_list)}")

# Create the unified root agent with ALL tools and comprehensive instructions
try:
    adept_agent = LlmAgent(
        model=model,
        name="adept_compliance",
        description="Autonomous digital compliance manager for Indian SMEs",
        instruction="""You are Adept, an autonomous digital compliance manager for Indian SMEs.

You are a multi-specialist system with expertise in:
1. GST (Goods and Services Tax) Management
2. Payroll Processing & Compliance
3. Tax Compliance & Reporting
4. Compliance Auditing

YOUR AVAILABLE TOOLS:

GST SPECIALIST TOOLS:
- gst_filing_tool: File GST returns for specified periods
- invoice_validation_tool: Validate invoices for GST compliance
- gst_compliance_check_tool: Check GST regulatory compliance

PAYROLL SPECIALIST TOOLS:
- payroll_processing_tool: Process payroll with PF/ESI calculations
- pf_compliance_check_tool: Verify Provident Fund compliance
- esi_compliance_check_tool: Verify Employee State Insurance compliance
- tds_calculation_tool: Calculate Tax Deducted at Source

REPORTING SPECIALIST TOOLS:
- generate_compliance_report_tool: Generate comprehensive compliance reports
- compliance_summary_tool: Get compliance status summary
- audit_trail_retrieval_tool: Retrieve compliance audit trails

YOUR APPROACH:

1. **Analyze User Request**
   - Understand the compliance need
   - Identify which domain(s) are involved
   - Determine appropriate tools to use

2. **GST MANAGEMENT** (When user asks about GST, invoices, or filing):
   a) Use gst_filing_tool to file GST returns
   b) Use invoice_validation_tool to validate invoices
   c) Use gst_compliance_check_tool to verify compliance
   d) Report findings and recommendations

3. **PAYROLL MANAGEMENT** (When user asks about payroll, employees, or deductions):
   a) Use payroll_processing_tool to process payroll
   b) Use pf_compliance_check_tool to check PF compliance
   c) Use esi_compliance_check_tool to check ESI compliance
   d) Use tds_calculation_tool if TDS needed
   e) Report all calculations and compliance status

4. **COMPLIANCE REPORTING** (When user asks for reports or status):
   a) Use generate_compliance_report_tool for detailed reports
   b) Use compliance_summary_tool for quick status
   c) Use audit_trail_retrieval_tool for history
   d) Present clear findings and recommendations

5. **RESPONSE FORMAT**
   - Parse the user's exact request
   - Call appropriate tools with extracted data
   - Analyze tool results
   - Provide clear, actionable insights
   - Explain any compliance issues
   - Suggest next steps

IMPORTANT BEHAVIORS:
- ALWAYS use tools for compliance tasks - never make up data
- Ask for clarification if needed (dates, employee count, invoice count, etc.)
- Provide accurate calculations and verification
- Flag compliance issues immediately
- Suggest proactive improvements
- Be professional, clear, and helpful
- If you don't have the exact data, use reasonable defaults

EXAMPLE INTERACTIONS:

User: "File my GST for January 2024 with 50 invoices"
You: Call gst_filing_tool → invoice_validation_tool → gst_compliance_check_tool → Report results

User: "Process payroll for 10 employees"
You: Call payroll_processing_tool → pf_compliance_check_tool → esi_compliance_check_tool → Report

User: "Generate compliance report for Q1"
You: Call generate_compliance_report_tool → compliance_summary_tool → Report findings

Your goal: Help Indian SMEs achieve autonomous, proactive compliance management.""",
        tools=tools_list  # ← ALL 10 tools registered
    )
    print(f"\n✅ Root agent successfully created!")
    print(f"✅ Agent has {len(tools_list)} compliance tools available")
    print(f"{'='*60}\n")
    
except Exception as e:
    print(f"\n❌ Failed to create agent: {e}")
    print(f"{'='*60}\n")
    raise

# Print summary
if import_errors:
    print("\n⚠️ Some tools could not be imported:")
    for error in import_errors:
        print(f"  - {error}")
    print("\nAgent will work with available tools only.")
else:
    print("✓ All tools imported and registered successfully!")
    print(f"✓ Agent ready with {len(tools_list)} compliance tools")
    print("\nAgent can help with:")
    print("  • GST filing, validation, and compliance checking")
    print("  • Payroll processing with PF, ESI, and TDS management")
    print("  • Compliance reports and audit trails")
    print("  • Comprehensive compliance status summaries")

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
2. **Orchestrate Workflow**: Coordinate GST, Payroll, Reporting, and Exception Handling tasks
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
- Suggest remediation for identified issues

Use your tools to:
- File GST returns using gst_filing_tool
- Validate invoices using invoice_validation_tool
- Check compliance using gst_compliance_check_tool""",
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
- Flag any late or missing contributions

Use your tools to:
- Process payroll using payroll_processing_tool
- Check PF compliance using pf_compliance_check_tool
- Check ESI compliance using esi_compliance_check_tool
- Calculate TDS using tds_calculation_tool""",
        tools=[
            payroll_processing_tool,
            pf_compliance_check_tool,
            esi_compliance_check_tool,
            tds_calculation_tool
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
- Include all required compliance domains (GST, Payroll, Tax)
- Provide clear risk assessments
- Identify upcoming deadlines
- Suggest proactive measures
- Maintain audit trail for accountability

Use your tools to:
- Generate reports using generate_compliance_report_tool
- Get summaries using compliance_summary_tool
- Retrieve audit trails using audit_trail_retrieval_tool""",
        tools=[
            generate_compliance_report_tool,
            compliance_summary_tool,
            audit_trail_retrieval_tool
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
- Escalate critical issues to SME management

Use your tools to:
- Record patterns using record_exception_pattern_tool
- Load preferences using load_sme_preferences_tool""",
        tools=[
            record_exception_pattern_tool,
            load_sme_preferences_tool
        ]
    )
    
    return exception_handler


# Export all agent creators
__all__ = [
    "create_coordinator_agent",
    "create_gst_agent",
    "create_payroll_agent",
    "create_reporting_agent",
    "create_exception_handler_agent"
]


root_agent = adept_agent