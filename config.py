"""
Configuration settings for Adept compliance system
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
MODEL = "gemini-2.0-flash"

# Project Configuration
PROJECT_NAME = os.getenv("PROJECT_NAME", "adept-compliance")
APP_NAME = os.getenv("APP_NAME", "adept_sme")

# Session Configuration
USER_ID = os.getenv("USER_ID", "sme_001")
SESSION_ID = os.getenv("SESSION_ID", "session_001")

# SME Configuration
SME_ID = os.getenv("SME_ID", "SME_001")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Sample Company")
GST_NUMBER = os.getenv("GST_NUMBER", "GST_00000")

# Agent Names
COORDINATOR_AGENT_NAME = "coordinator"
GST_AGENT_NAME = "gst_specialist"
PAYROLL_AGENT_NAME = "payroll_specialist"
REPORTING_AGENT_NAME = "reporting_specialist"
EXCEPTION_HANDLER_NAME = "exception_handler"

# Initial Session State
INITIAL_STATE = {
    "sme_id": SME_ID,
    "company_name": COMPANY_NAME,
    "gst_number": GST_NUMBER,
    "compliance_status": {},
    "preferences": {
        "filing_frequency": "monthly",
        "risk_tolerance": "low",
        "exception_handling": "proactive",
        "notification_method": "email"
    },
    "exception_log": [],
    "compliance_history": [],
    "regulatory_changes": []
}
