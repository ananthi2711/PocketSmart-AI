"""
PocketSmart AI - Application Configuration & Settings
"""

import os
from pathlib import Path

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if python-dotenv is available
env_path = BASE_DIR / ".env"
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path, override=True)
except ImportError:
    pass


# Application Metadata
APP_TITLE = "PocketSmart AI"
APP_SUBTITLE = "Your Smart Budget & Recommendation Assistant"
APP_ICON = "💰"
CURRENCY_SYMBOL = "₹"

# Educational & Legal Disclaimer
FINANCIAL_DISCLAIMER = (
    "This application provides educational budgeting guidance and is not professional financial advice."
)

def _get_setting(key: str, default: str = "") -> str:
    """Retrieve setting from environment variable or Streamlit secrets."""
    val = os.getenv(key)
    if val and val.strip():
        return val.strip()
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return default


# Gemini AI Model Configuration
GEMINI_API_KEY = _get_setting("GEMINI_API_KEY", "")
GEMINI_MODEL = _get_setting("GEMINI_MODEL", "gemini-1.5-flash")

# Predefined Expense Categories
EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Utilities",
    "Shopping",
    "Housing",
    "Education",
    "Entertainment",
    "Health",
    "Other",
]

# Category Keyword Mapping for Automatic Categorization
CATEGORY_KEYWORDS = {
    "Food": [
        "food", "grocery", "groceries", "supermarket", "lunch", "dinner",
        "breakfast", "snack", "snacks", "coffee", "tea", "cafe", "restaurant",
        "swiggy", "zomato", "dining", "meal", "pizza", "burger", "drinks",
        "milk", "vegetables", "fruits", "meat", "bread"
    ],
    "Transport": [
        "transport", "travel", "petrol", "diesel", "fuel", "gasoline", "cab",
        "taxi", "uber", "ola", "bus", "train", "metro", "auto", "flight",
        "airfare", "parking", "toll", "commute", "bike", "car"
    ],
    "Utilities": [
        "electricity", "water", "gas", "cylinder", "internet", "wifi",
        "broadband", "phone", "mobile", "recharge", "bill", "bills",
        "dth", "power", "utility"
    ],
    "Shopping": [
        "shopping", "clothes", "clothing", "dress", "shirt", "pant", "shoes",
        "amazon", "flipkart", "myntra", "electronics", "gadget", "watch",
        "accessories", "retail", "mall", "purchase"
    ],
    "Housing": [
        "rent", "housing", "maintenance", "society", "flat", "apartment",
        "mortgage", "lease", "repair", "plumber", "electrician", "property"
    ],
    "Education": [
        "education", "course", "books", "book", "tuition", "fees", "fee",
        "school", "college", "university", "udemy", "coursera", "stationery",
        "exam", "classes", "training"
    ],
    "Entertainment": [
        "entertainment", "movie", "movies", "cinema", "theatre", "netflix",
        "prime", "hotstar", "spotify", "music", "game", "gaming", "steam",
        "concert", "party", "club", "outing", "hobbies"
    ],
    "Health": [
        "health", "medicine", "medicines", "medical", "doctor", "clinic",
        "hospital", "pharmacy", "gym", "fitness", "yoga", "dental",
        "checkup", "test", "lab"
    ],
    "Other": []
}

# Event Planning Baseline Allocations (%)
EVENT_TYPES = [
    "Birthday Party",
    "College Event",
    "Family Function",
    "Other"
]

EVENT_BASELINE_SPLITS = {
    "Birthday Party": {
        "Food": 40,
        "Venue": 25,
        "Decoration": 15,
        "Activities": 10,
        "Miscellaneous": 10,
    },
    "College Event": {
        "Food": 30,
        "Venue": 25,
        "Decoration": 15,
        "Activities": 20,
        "Miscellaneous": 10,
    },
    "Family Function": {
        "Food": 45,
        "Venue": 30,
        "Decoration": 10,
        "Activities": 5,
        "Miscellaneous": 10,
    },
    "Other": {
        "Food": 35,
        "Venue": 25,
        "Decoration": 15,
        "Activities": 15,
        "Miscellaneous": 10,
    },
}

# Jewellery Matching Options
JEWELLERY_STYLES = [
    "Minimal",
    "Traditional",
    "Modern",
    "Party Wear",
    "Any"
]

SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png"]


def is_gemini_configured(api_key: str = None) -> bool:
    """Check if a non-empty Gemini API key is configured."""
    key = api_key if api_key is not None else GEMINI_API_KEY
    return bool(key and key.strip() and key.strip() != "your_api_key_here")
