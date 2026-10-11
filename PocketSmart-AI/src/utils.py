"""
PocketSmart AI - Utility Functions
Provides expense parsing, categorization, financial calculations,
sensitive data masking, input validation, and PDF report generation.
"""

import re
from typing import Dict, List, Tuple, Any, Optional
from config.settings import CATEGORY_KEYWORDS, EXPENSE_CATEGORIES, FINANCIAL_DISCLAIMER


# =====================================================================
# SENSITIVE DATA MASKING & SECURITY
# =====================================================================

def mask_sensitive_data(text: str) -> str:
    """
    Masks personally identifiable or sensitive numeric patterns such as
    phone numbers, credit/debit card numbers, account numbers, and email addresses.
    Ensures safe transmission to AI models.
    """
    if not text:
        return ""

    sanitized = text

    # Mask email addresses
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    sanitized = re.sub(email_pattern, "[EMAIL_MASKED]", sanitized)

    # Mask credit/debit card numbers (13 to 19 digits, possibly separated by spaces or hyphens)
    card_pattern = r"\b(?:\d{4}[ -]?){3}\d{1,4}\b|\b\d{13,19}\b"
    sanitized = re.sub(card_pattern, "[CARD_MASKED]", sanitized)

    # Mask 10-digit mobile / phone numbers with optional country code (+91, etc.)
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b[6-9]\d{9}\b"
    sanitized = re.sub(phone_pattern, "[PHONE_MASKED]", sanitized)

    return sanitized


# =====================================================================
# CATEGORY DETECTION
# =====================================================================

def detect_category(item_name: str) -> str:
    """
    Intelligently assigns an expense category based on keywords in the item name.
    Falls back to 'Other' if no keyword matches.
    """
    cleaned_name = item_name.lower().strip()

    # Exact or substring match in keyword dictionary
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == "Other":
            continue
        for kw in keywords:
            # Check for word boundary or direct inclusion
            if re.search(r"\b" + re.escape(kw) + r"\b", cleaned_name) or kw in cleaned_name:
                return category

    return "Other"


# =====================================================================
# EXPENSE PARSING & VALIDATION
# =====================================================================

def parse_expenses_text(text: str) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
    """
    Parses multi-line text input containing expenses in various common formats:
      - Food 250
      - Food: 250
      - Food - 250
      - Food = 250
      - Food, 250
      - Food Rs. 250 / Food ₹250

    Returns:
      - valid_items: list of dicts with item, amount, category, raw_line
      - invalid_lines: lines that could not be parsed
      - warnings: list of non-critical warnings (e.g. negative numbers rejected)
    """
    valid_items: List[Dict[str, Any]] = []
    invalid_lines: List[str] = []
    warnings: List[str] = []

    if not text or not text.strip():
        return valid_items, invalid_lines, ["No expense text provided."]

    # Regex pattern:
    # Captures label (letters, spaces) followed by optional separator (:, -, =, ,)
    # followed by optional currency symbol (Rs. / ₹ / INR / $), followed by numeric amount
    pattern = re.compile(
        r"^(?P<label>[\w\s&'/]+?)\s*[:\-=,]?\s*(?:(?:rs\.?|inr|₹|\$)\s*)?(?P<amount>-?\d+(?:\.\d+)?)\s*$",
        re.IGNORECASE
    )

    for line_num, line in enumerate(text.splitlines(), start=1):
        raw_line = line.strip()
        if not raw_line or raw_line.startswith("#"):
            continue  # Ignore empty lines and comments

        match = pattern.match(raw_line)
        if match:
            label = match.group("label").strip()
            amount_str = match.group("amount").strip()

            try:
                amount = float(amount_str)
                if amount < 0:
                    warnings.append(f"Line {line_num}: Negative amount skipped: '{raw_line}'")
                    continue
                if amount == 0:
                    warnings.append(f"Line {line_num}: Zero amount skipped: '{raw_line}'")
                    continue

                category = detect_category(label)
                valid_items.append({
                    "item": label.title(),
                    "amount": round(amount, 2),
                    "category": category,
                    "raw_line": raw_line
                })
            except ValueError:
                invalid_lines.append(f"Line {line_num}: '{raw_line}' (invalid number)")
        else:
            invalid_lines.append(f"Line {line_num}: '{raw_line}'")

    return valid_items, invalid_lines, warnings


# =====================================================================
# FINANCIAL CALCULATIONS
# =====================================================================

def calculate_budget_summary(income: float, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates total expenses, category-wise breakdown, remaining balance,
    and savings rate percentage.
    """
    total_expenses = round(sum(item["amount"] for item in items), 2)
    remaining_balance = round(income - total_expenses, 2)

    savings_rate = 0.0
    if income > 0:
        savings_rate = round((remaining_balance / income) * 100, 2)

    # Initialize all standard categories with 0.0
    category_totals: Dict[str, float] = {cat: 0.0 for cat in EXPENSE_CATEGORIES}

    for item in items:
        cat = item["category"]
        if cat in category_totals:
            category_totals[cat] = round(category_totals[cat] + item["amount"], 2)
        else:
            category_totals["Other"] = round(category_totals.get("Other", 0.0) + item["amount"], 2)

    # Filter out categories with 0 spend for compact reporting, but keep in breakdown
    active_category_totals = {k: v for k, v in category_totals.items() if v > 0}

    # Calculate category percentages
    category_percentages: Dict[str, float] = {}
    for cat, amt in active_category_totals.items():
        pct = round((amt / total_expenses) * 100, 1) if total_expenses > 0 else 0.0
        category_percentages[cat] = pct

    # Financial health status
    if remaining_balance < 0:
        health_status = "Deficit"
        status_color = "#EF4444"  # Red
        status_message = "Your expenses exceed your monthly income. Immediate cost reduction is recommended."
    elif remaining_balance == 0:
        health_status = "Break-even"
        status_color = "#F59E0B"  # Amber
        status_message = "You are spending 100% of your income. Aim to build a safety buffer."
    elif savings_rate < 20:
        health_status = "Tight Margin"
        status_color = "#F59E0B"  # Amber
        status_message = "Your savings rate is below the recommended 20% benchmark."
    else:
        health_status = "Healthy"
        status_color = "#10B981"  # Emerald Green
        status_message = "Great job! You are maintaining a healthy savings surplus."

    return {
        "income": round(income, 2),
        "total_expenses": total_expenses,
        "remaining_balance": remaining_balance,
        "savings_rate": savings_rate,
        "category_totals": active_category_totals,
        "all_category_totals": category_totals,
        "category_percentages": category_percentages,
        "health_status": health_status,
        "status_color": status_color,
        "status_message": status_message,
        "item_count": len(items)
    }


# =====================================================================
# PDF REPORT GENERATOR (FPDF2)
# =====================================================================

def generate_budget_pdf_report(
    summary: Dict[str, Any],
    items: List[Dict[str, Any]],
    ai_recommendations: str
) -> Optional[bytes]:
    """
    Generates a structured PDF Budget Report using FPDF.
    Returns bytes for direct download via Streamlit.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        # FPDF not available
        return None

    class BudgetPDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(16, 185, 129)  # Emerald color
            self.cell(0, 10, "PocketSmart AI - Monthly Budget Report", ln=True, align="C")
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(100, 116, 139)
            self.cell(0, 5, "Your Smart Budget & Recommendation Assistant", ln=True, align="C")
            self.line(10, 26, 200, 26)
            self.ln(6)

        def footer(self):
            self.set_y(-18)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 5, FINANCIAL_DISCLAIMER, ln=True, align="C")
            self.cell(0, 5, f"Page {self.page_no()}", align="C")

    pdf = BudgetPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Section 1: Financial Summary Cards
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. Executive Financial Summary", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_fill_color(248, 250, 252)

    col_w = 47
    pdf.cell(col_w, 8, f"Income: Rs. {summary['income']:,.2f}", border=1, fill=True)
    pdf.cell(col_w, 8, f"Expenses: Rs. {summary['total_expenses']:,.2f}", border=1, fill=True)
    pdf.cell(col_w, 8, f"Balance: Rs. {summary['remaining_balance']:,.2f}", border=1, fill=True)
    pdf.cell(col_w, 8, f"Savings Rate: {summary['savings_rate']}%", border=1, fill=True, ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 6, "Financial Health: ")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"{summary['health_status']} - {summary['status_message']}", ln=True)

    pdf.ln(4)

    # Section 2: Category Breakdown Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "2. Category-Wise Breakdown", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(226, 232, 240)
    pdf.cell(90, 7, "Category", border=1, fill=True)
    pdf.cell(50, 7, "Amount (Rs.)", border=1, fill=True)
    pdf.cell(50, 7, "Share (%)", border=1, fill=True, ln=True)

    pdf.set_font("Helvetica", "", 10)
    for cat, amt in summary["category_totals"].items():
        pct = summary["category_percentages"].get(cat, 0.0)
        pdf.cell(90, 6, cat, border=1)
        pdf.cell(50, 6, f"Rs. {amt:,.2f}", border=1)
        pdf.cell(50, 6, f"{pct:.1f}%", border=1, ln=True)

    pdf.ln(6)

    # Section 3: AI Saving Strategies & Recommendations
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "3. Personalized AI Saving Strategies & Action Plan", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 9)
    # Clean text to avoid encoding errors in standard fpdf
    clean_ai_text = ai_recommendations.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 5, clean_ai_text)

    # Output bytes
    try:
        # fpdf2 supports output() returning bytearray or bytes
        pdf_bytes = bytes(pdf.output())
        return pdf_bytes
    except Exception:
        return None
