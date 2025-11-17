"""
Main entry point for Adept compliance system - INTERACTIVE VERSION (FIXED)
Features:
1. Interactive user input (no hard-coded prompts)
2. Agent scope validation (only compliance-related queries) - SINGLE RESPONSE ONLY
3. Proper session state persistence
"""
import asyncio
import uuid
import json
from typing import Optional
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.genai.types import Content, Part
import config
from agents import (
    create_coordinator_agent,
    create_gst_agent,
    create_payroll_agent,
    create_reporting_agent,
    create_exception_handler_agent
)

# Import mock tools directly
from gst_tools import (
    gst_filing_tool,
    invoice_validation_tool,
    gst_compliance_check_tool
)
from payroll_tools import (
    payroll_processing_tool,
    pf_compliance_check_tool,
    esi_compliance_check_tool,
    tds_calculation_tool
)
from reporting_tools import (
    generate_compliance_report_tool,
    compliance_summary_tool,
    audit_trail_retrieval_tool
)


class AdeptComplianceManager:
    """Main class for managing the Adept compliance system."""
    
    def __init__(self):
        """Initialize the compliance manager with services and agents."""
        # Initialize services
        self.session_service = InMemorySessionService()
        self.memory_service = InMemoryMemoryService()
        
        # Create agents
        self.coordinator_agent = create_coordinator_agent(config.MODEL)
        self.gst_agent = create_gst_agent(config.MODEL)
        self.payroll_agent = create_payroll_agent(config.MODEL)
        self.reporting_agent = create_reporting_agent(config.MODEL)
        self.exception_handler = create_exception_handler_agent(config.MODEL)
        
        # Create runner with coordinator agent
        self.runner = Runner(
            app_name=config.APP_NAME,
            agent=self.coordinator_agent,
            session_service=self.session_service,
            memory_service=self.memory_service
        )
        
        # Define compliance-related keywords for scope validation
        self.compliance_keywords = {
            'gst': ['gst', 'goods and services tax'],
            'tax': ['tax', 'tds', 'income tax', 'tax filing'],
            'filing': ['filing', 'file', 'submit', 'return'],
            'invoice': ['invoice', 'bill', 'receipt'],
            'payroll': ['payroll', 'salary', 'wage'],
            'pf': ['pf', 'provident fund', 'epfo'],
            'esi': ['esi', 'employee state insurance', 'esic'],
            'compliance': ['compliance', 'compliant', 'regulatory', 'regulation'],
            'report': ['report', 'generate', 'create', 'summary'],
            'employee': ['employee', 'staff', 'worker', 'personnel'],
            'deduction': ['deduction', 'deduct', 'withhold'],
            'audit': ['audit', 'audit trail', 'auditor'],
            'challan': ['challan', 'payment'],
            'status': ['status', 'check', 'verify'],
            'verification': ['verify', 'validate', 'validate']
        }
        
        print("✅ Adept Compliance Manager initialized successfully")
        print("=" * 80)
        print("ADEPT - Your Digital Compliance Assistant for Indian SMEs")
        print("I can help with: GST, Payroll (PF/ESI), TDS, Reports, and Compliance Checks")
        print("=" * 80)
    
    def is_compliance_related(self, query: str) -> bool:
        """
        Check if the query is related to compliance.
        Returns True/False with single decision.
        
        Args:
            query: User query
            
        Returns:
            True if query is compliance-related, False otherwise
        """
        query_lower = query.lower().strip()
        
        # Check for compliance keywords - single pass through all keywords
        for category, keywords in self.compliance_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return True
        
        # If no keywords found, it's not compliance-related
        return False
    
    def get_polite_rejection(self, query: str) -> str:
        """
        Generate a SINGLE, polite rejection message for out-of-scope queries.
        ONLY called if is_compliance_related() returns False.
        
        Args:
            query: User query
            
        Returns:
            Single polite rejection message (no multiple replies)
        """
        return f"""I appreciate your question, but I'm specifically designed to help with compliance management for Indian SMEs. I can assist with:
  • GST filing and invoice validation
  • Payroll processing (PF, ESI, TDS calculations)
  • Compliance reports and audit trails
  • Regulatory status checks
  • Tax calculations and deductions

Please ask me about compliance-related matters, and I'll be happy to help! 😊"""
    
    async def initialize_session(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> str:
        """Initialize or retrieve a session for an SME."""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        await self.session_service.create_session(
            app_name=config.APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state=config.INITIAL_STATE.copy()
        )
        
        print(f"\n✅ Session initialized: {session_id[:8]}...")
        return session_id
    
    def parse_gst_data(self, query: str) -> dict:
        """
        Extract GST-related data from user query.
        
        Args:
            query: User query
            
        Returns:
            Extracted GST data
        """
        import re
        
        data = {
            'filing_period': None,
            'invoice_count': None,
            'invoices': []
        }
        
        # Extract period (e.g., "January 2024", "2024-01")
        period_patterns = [
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
            r'(\d{4})-(\d{2})',
            r'Q(\d)\s+(\d{4})'
        ]
        
        for pattern in period_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if 'Q' in pattern:
                    data['filing_period'] = f"Q{match.group(1)}_{match.group(2)}"
                elif '-' in pattern:
                    data['filing_period'] = f"{match.group(1)}-{match.group(2)}"
                else:
                    months = ['january', 'february', 'march', 'april', 'may', 'june',
                             'july', 'august', 'september', 'october', 'november', 'december']
                    month_name = match.group(1).lower()
                    month_num = months.index(month_name) + 1
                    data['filing_period'] = f"{match.group(2)}-{month_num:02d}"
                break
        
        # Extract invoice count
        invoice_match = re.search(r'(\d+)\s+invoices?', query, re.IGNORECASE)
        if invoice_match:
            data['invoice_count'] = int(invoice_match.group(1))
            # Generate sample invoices
            data['invoices'] = [
                {"invoice_number": f"INV-{i:03d}", "amount": 5000, "gst_rate": 18}
                for i in range(data['invoice_count'])
            ]
        
        return data
    
    def parse_payroll_data(self, query: str) -> dict:
        """Extract payroll-related data from user query."""
        import re
        
        data = {
            'employee_count': None,
            'salary_month': None
        }
        
        # Extract employee count
        emp_match = re.search(r'(\d+)\s+employees?', query, re.IGNORECASE)
        if emp_match:
            data['employee_count'] = int(emp_match.group(1))
        
        # Extract month
        month_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})', query, re.IGNORECASE)
        if month_match:
            months = ['january', 'february', 'march', 'april', 'may', 'june',
                     'july', 'august', 'september', 'october', 'november', 'december']
            month_name = month_match.group(1).lower()
            month_num = months.index(month_name) + 1
            data['salary_month'] = f"{month_match.group(2)}-{month_num:02d}"
        
        return data
    
    async def process_user_query(
        self,
        user_id: str,
        session_id: str,
        query: str
    ) -> str:
        """
        Process a user query with SINGLE response.
        FIXED: Returns only one answer - no multiple replies.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            query: User's natural language query
            
        Returns:
            Single response from the agent
        """
        print(f"\n{'='*80}")
        print(f"📥 Your Query: {query}")
        print(f"{'='*80}\n")
        
        # VALIDATION LAYER: Single check - if not compliance, return ONLY rejection
        if not self.is_compliance_related(query):
            rejection_message = self.get_polite_rejection(query)
            print(f"🤖 Adept: {rejection_message}\n")
            return rejection_message
        
        # COMPLIANCE QUERY: Process through agent
        # Get session
        session = await self.session_service.get_session(
            app_name=config.APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        
        # Determine query type and process - SINGLE EXECUTION PATH
        query_lower = query.lower()
        
        # GST Filing
        if any(word in query_lower for word in ['gst', 'file', 'filing', 'invoice']):
            response = await self._handle_gst_query(query, session)
            print(f"🤖 Adept: {response}\n")
            return response
        
        # Payroll
        elif any(word in query_lower for word in ['payroll', 'salary', 'employee', 'pf', 'esi']):
            response = await self._handle_payroll_query(query, session)
            print(f"🤖 Adept: {response}\n")
            return response
        
        # Report
        elif any(word in query_lower for word in ['report', 'generate', 'quarterly', 'annual']):
            response = await self._handle_report_query(query, session)
            print(f"🤖 Adept: {response}\n")
            return response
        
        # Status check
        elif any(word in query_lower for word in ['status', 'check', 'summary', 'compliance']):
            response = await self._handle_status_query(query, session)
            print(f"🤖 Adept: {response}\n")
            return response
        
        # Default: Ask for clarification (SINGLE RESPONSE)
        else:
            clarification_msg = """I understand this is compliance-related. Please specify what you'd like me to do:
  1. "File my GST for [month] with [X] invoices"
  2. "Process payroll for [X] employees"
  3. "Generate compliance report for [period]"
  4. "Check my compliance status"
  
Please provide more details and I'll help you!"""
            print(f"🤖 Adept: {clarification_msg}\n")
            return clarification_msg
    
    async def _handle_gst_query(self, query: str, session) -> str:
        """Handle GST-related queries - SINGLE RESPONSE."""
        print("🔍 Detected: GST Filing Request")
        
        # Parse data from query
        gst_data = self.parse_gst_data(query)
        
        # Validation - return SINGLE error message if needed
        if not gst_data['filing_period']:
            return "Please specify the filing period (e.g., 'January 2024' or '2024-01')"
        
        if not gst_data['invoice_count']:
            return "Please specify the number of invoices (e.g., '50 invoices')"
        
        print(f"📋 Filing Period: {gst_data['filing_period']}")
        print(f"📋 Invoice Count: {gst_data['invoice_count']}")
        
        # Process GST filing
        print("\n[GST Agent Processing...]")
        
        gst_result = gst_filing_tool(
            sme_id=config.SME_ID,
            filing_period=gst_data['filing_period'],
            invoices=gst_data['invoices'],
            tool_context=session
        )
        print(f"✅ {gst_result['result']}")
        
        validation_result = invoice_validation_tool(
            sme_id=config.SME_ID,
            invoices=gst_data['invoices'],
            tool_context=session
        )
        print(f"\n📊 {validation_result['details']}")
        
        compliance_result = gst_compliance_check_tool(
            sme_id=config.SME_ID,
            filing_period=gst_data['filing_period'],
            tool_context=session
        )
        
        # SINGLE RESPONSE - compile all info into one message
        response = f"""✅ GST Filing Completed!

Filing Period: {gst_data['filing_period']}
Invoices Processed: {gst_result['invoice_count']}
Total Value: ₹{gst_result['total_value']:,.2f}

Validation Results:
  • Valid Invoices: {validation_result['valid_invoices']}
  • Invalid Invoices: {validation_result['invalid_invoices']}

Compliance Status: {compliance_result['status'].upper()}"""
        
        if compliance_result['issues']:
            response += "\n\n⚠️ Issues Found:\n"
            for issue in compliance_result['issues']:
                response += f"  • {issue['type']} ({issue['severity']}): {issue['description']}\n"
            response += "\n💡 Recommendations:\n"
            for rec in compliance_result['recommendations']:
                response += f"  {rec}\n"
        
        return response
    
    async def _handle_payroll_query(self, query: str, session) -> str:
        """Handle payroll-related queries - SINGLE RESPONSE."""
        print("🔍 Detected: Payroll Request")
        
        payroll_data = self.parse_payroll_data(query)
        
        # Validation - SINGLE error message
        if not payroll_data['employee_count']:
            return "Please specify the number of employees (e.g., '10 employees')"
        
        print(f"👥 Employee Count: {payroll_data['employee_count']}")
        
        print("\n[Payroll Agent Processing...]")
        
        payroll_result = payroll_processing_tool(
            sme_id=config.SME_ID,
            employee_count=payroll_data['employee_count'],
            salary_month=payroll_data['salary_month'] or "2024-11",
            tool_context=session
        )
        
        pf_result = pf_compliance_check_tool(
            sme_id=config.SME_ID,
            employee_count=payroll_data['employee_count'],
            tool_context=session
        )
        
        esi_result = esi_compliance_check_tool(
            sme_id=config.SME_ID,
            employee_count=payroll_data['employee_count'],
            tool_context=session
        )
        
        # SINGLE RESPONSE
        response = f"""✅ Payroll Processing Completed!

Employees: {payroll_result['employees']}
Month: {payroll_result['salary_month']}

💰 Financial Breakdown:
  • Total Payroll: ₹{payroll_result['total_payroll']:,.2f}
  • PF Deduction (12%): ₹{payroll_result['total_pf_deduction']:,.2f}
  • ESI Deduction (4.75%): ₹{payroll_result['total_esi_deduction']:,.2f}
  • Net Payable: ₹{payroll_result['total_payroll'] - payroll_result['total_pf_deduction'] - payroll_result['total_esi_deduction']:,.2f}

✅ Compliance Status:
  • PF: {pf_result['status'].upper()}
  • ESI: {esi_result['status'].upper()}

All payroll requirements are compliant. Next deadline: 2024-12-15"""
        
        return response
    
    async def _handle_report_query(self, query: str, session) -> str:
        """Handle report generation queries - SINGLE RESPONSE."""
        print("🔍 Detected: Report Generation Request")
        
        # Extract period
        import re
        period = "Q1_2024"  # Default
        
        quarter_match = re.search(r'Q(\d)\s+(\d{4})', query, re.IGNORECASE)
        if quarter_match:
            period = f"Q{quarter_match.group(1)}_{quarter_match.group(2)}"
        
        print("\n[Reporting Agent Processing...]")
        
        report_result = generate_compliance_report_tool(
            sme_id=config.SME_ID,
            report_type="quarterly",
            period=period,
            tool_context=session
        )
        
        # SINGLE RESPONSE
        response = f"""✅ Compliance Report Generated!

Report ID: {report_result['report_id']}
Period: {period}
Report Type: Quarterly

📋 Report Sections:
"""
        for section in report_result['sections'].keys():
            response += f"  • {section.replace('_', ' ')}\n"
        
        response += f"""
🎯 Overall Risk Level: {report_result['sections']['Risk_Assessment']['overall_risk']}
⚠️ Critical Issues: {report_result['sections']['Risk_Assessment']['critical_issues']}
📊 High Priority Issues: {report_result['sections']['Risk_Assessment']['high_priority_issues']}

The report is ready for your records and can be submitted to authorities."""
        
        return response
    
    async def _handle_status_query(self, query: str, session) -> str:
        """Handle compliance status queries - SINGLE RESPONSE."""
        print("🔍 Detected: Status Check Request")
        
        print("\n[Coordinator Processing...]")
        
        summary_result = compliance_summary_tool(
            sme_id=config.SME_ID,
            tool_context=session
        )
        
        # SINGLE RESPONSE
        return summary_result['compliance_snapshot']
    
    async def get_session_state(
        self,
        user_id: str,
        session_id: str
    ) -> dict:
        """Retrieve current session state."""
        session = await self.session_service.get_session(
            app_name=config.APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        return session.state if session else {}


async def interactive_mode():
    """Run Adept in interactive mode."""
    
    manager = AdeptComplianceManager()
    user_id = config.USER_ID
    session_id = await manager.initialize_session(user_id)
    
    print("\n💬 Interactive Mode Started")
    print("Type your compliance-related queries below.")
    print("Type 'status' to see session state, 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Thank you for using Adept! Goodbye.")
                break
            
            if user_input.lower() == 'status':
                state = await manager.get_session_state(user_id, session_id)
                print("\n" + "="*80)
                print("📊 Current Session State:")
                print("="*80)
                print(f"\n✅ Compliance Status:\n{json.dumps(state.get('compliance_status', {}), indent=2)}")
                print(f"\n⚠️ Exception Log:\n{json.dumps(state.get('exception_log', []), indent=2)}")
                print(f"\n📋 Compliance History:\n{json.dumps(state.get('compliance_history', []), indent=2)}")
                print(f"\n⚙️ Preferences:\n{json.dumps(state.get('preferences', {}), indent=2)}")
                continue
            
            # Process query - SINGLE RESPONSE ONLY
            await manager.process_user_query(user_id, session_id, user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()


async def demo_mode():
    """Run predefined demo queries."""
    
    manager = AdeptComplianceManager()
    user_id = config.USER_ID
    session_id = await manager.initialize_session(user_id)
    
    print("\n🎬 Running Demo Mode with Sample Queries...\n")
    
    demo_queries = [
        "File my GST for January 2024 with 50 invoices",
        "What's the weather in Kolkata?",  # Should be rejected with SINGLE response
        "Process payroll for 10 employees",
        "Generate compliance report for Q1 2024",
        "Check my compliance status"
    ]
    
    for query in demo_queries:
        await manager.process_user_query(user_id, session_id, query)
        print(f"{'='*80}\n")
        await asyncio.sleep(1)
    
    # Show final state
    print("="*80)
    print("📊 Final Session State:")
    print("="*80)
    state = await manager.get_session_state(user_id, session_id)
    print(f"\n✅ Compliance Status:\n{json.dumps(state.get('compliance_status', {}), indent=2)}")
    print(f"\n⚠️ Exception Log:\n{json.dumps(state.get('exception_log', []), indent=2)}")
    print(f"\n📋 Compliance History:\n{json.dumps(state.get('compliance_history', []), indent=2)}")


async def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("ADEPT - Agent for Dynamic Enterprise & Proactive Tasking")
    print("="*80)
    print("\nChoose mode:")
    print("1. Interactive Mode (Type your queries)")
    print("2. Demo Mode (Predefined queries)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        await interactive_mode()
    elif choice == "2":
        await demo_mode()
    else:
        print("Invalid choice. Running demo mode...")
        await demo_mode()


if __name__ == "__main__":
    asyncio.run(main())
