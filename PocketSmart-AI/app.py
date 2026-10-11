"""
PocketSmart AI
"Your Smart Budget & Recommendation Assistant"

A comprehensive Streamlit application powered by Python, Streamlit, and Google Gemini.
Features:
  1. Smart Budget Analyzer
  2. AI Event Cost Estimator
  3. AI Jewellery Matcher
Includes dark glow styling, input validation, sensitive data masking, and safe Demo Fallbacks.
"""

import streamlit as st
import pandas as pd
from PIL import Image
import altair as alt

from config.settings import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    CURRENCY_SYMBOL,
    FINANCIAL_DISCLAIMER,
    EVENT_TYPES,
    JEWELLERY_STYLES,
    SUPPORTED_IMAGE_FORMATS,
    GEMINI_MODEL,
    is_gemini_configured,
)
from style import apply_custom_styles, render_metric_card
from src.utils import (
    parse_expenses_text,
    calculate_budget_summary,
    generate_budget_pdf_report,
)
from src.ai_engine import (
    analyze_budget_with_gemini,
    estimate_event_budget,
    recommend_jewellery,
    configure_gemini,
)


# =====================================================================
# PAGE CONFIGURATION
# =====================================================================

st.set_page_config(
    page_title=f"{APP_TITLE} - {APP_SUBTITLE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply dark glow CSS
apply_custom_styles()


# =====================================================================
# SIDEBAR
# =====================================================================

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    st.markdown(f"*{APP_SUBTITLE}*")
    st.divider()

    # Session State Key Management
    if "user_api_key" not in st.session_state:
        st.session_state.user_api_key = ""

    st.markdown("### ⚙️ Gemini Configuration")
    user_key_input = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        value=st.session_state.user_api_key,
        help="Enter your Google Gemini API key. If left blank, PocketSmart AI runs in safe Demo Fallback Mode.",
        placeholder="AIzaSy...",
    )
    if user_key_input != st.session_state.user_api_key:
        st.session_state.user_api_key = user_key_input.strip()

    # Model status check
    active_key = st.session_state.user_api_key or None
    _, is_ready, status_msg = configure_gemini(active_key)

    if is_ready:
        st.markdown(
            '<div class="glow-badge badge-live">● Live AI Active (Gemini)</div>',
            unsafe_allow_html=True,
        )
        st.caption(f"Model: `{GEMINI_MODEL}`")
    else:
        st.markdown(
            '<div class="glow-badge badge-demo">● Demo Fallback Mode</div>',
            unsafe_allow_html=True,
        )
        st.caption("No API key detected. Running on local deterministic rules.")

    st.divider()

    # Quick Navigation / About
    st.markdown("### 📌 Capabilities")
    st.markdown(
        """
        - **Smart Budget Analyzer:** Auto-categorize expenses, track savings rate, and receive AI optimization plans.
        - **Event Cost Estimator:** AI-driven budget splits for parties, weddings, and functions.
        - **AI Jewellery Matcher:** Upload an outfit for personalized jewellery styling & budget allocation.
        """
    )

    st.divider()

    # Disclaimer
    st.caption(f"🛡️ **Educational Notice:** {FINANCIAL_DISCLAIMER}")


# =====================================================================
# MAIN HEADER
# =====================================================================

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(f'<div class="glow-header">{APP_ICON} {APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glow-subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

with header_col2:
    if is_ready:
        st.markdown(
            '<div style="text-align: right; padding-top: 15px;"><span class="glow-badge badge-live">Gemini AI Online</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="text-align: right; padding-top: 15px;"><span class="glow-badge badge-demo">Demo Mode Active</span></div>',
            unsafe_allow_html=True,
        )


# =====================================================================
# TABS
# =====================================================================

tab_budget, tab_event, tab_jewellery = st.tabs([
    "📊 Smart Budget Analyzer",
    "🎉 AI Event Cost Estimator",
    "💎 AI Jewellery Matcher"
])


# =====================================================================
# TAB 1: SMART BUDGET ANALYZER
# =====================================================================

with tab_budget:
    st.markdown("### 💰 Smart Monthly Budget & Expense Analyzer")
    st.markdown(
        "Enter your monthly income and paste your expense records. Supported formats include: "
        "`Food 250`, `Transport: 120`, `Rent - 8000`, `Electricity = 900`."
    )

    sample_expenses = """Food 250
Transport 120
Electricity 900
Shopping 600
Rent 8000
Groceries 2400
Wifi Bill 800
Netflix 499
Doctor Consultation 500"""

    col_input1, col_input2 = st.columns([1, 2])

    with col_input1:
        st.markdown("#### 1. Income Details")
        monthly_income = st.number_input(
            f"Monthly Income ({CURRENCY_SYMBOL})",
            min_value=0.0,
            value=25000.0,
            step=1000.0,
            format="%.2f",
            help="Enter your total monthly earnings or salary.",
        )

        st.markdown("#### 2. Expense Input")
        load_sample = st.button("📋 Load Sample Expenses")
        if "expense_text_content" not in st.session_state:
            st.session_state.expense_text_content = sample_expenses

        if load_sample:
            st.session_state.expense_text_content = sample_expenses

        expense_text = st.text_area(
            "Paste Expenses (one per line):",
            value=st.session_state.expense_text_content,
            height=240,
            placeholder="Food 250\nTransport 120\nElectricity 900\nShopping 600\nRent 8000",
        )

        btn_analyze = st.button("⚡ Analyze My Budget", use_container_width=True)

    with col_input2:
        if btn_analyze or ("budget_analyzed" in st.session_state and st.session_state.budget_analyzed):
            st.session_state.budget_analyzed = True

            # Parse input
            items, invalid_lines, warnings = parse_expenses_text(expense_text)

            # Display validation warnings
            if invalid_lines:
                with st.expander("⚠️ Some lines could not be parsed (click to view)", expanded=False):
                    for inv in invalid_lines:
                        st.markdown(f"- `{inv}`")
                    st.caption("Expected format: `Item <amount>` (e.g., `Dinner 450`)")

            if warnings:
                with st.expander("ℹ️ Notes on input values", expanded=False):
                    for w in warnings:
                        st.markdown(f"- {w}")

            if not items:
                st.error("No valid expense entries found. Please enter at least one valid line (e.g., `Food 250`).")
            else:
                summary = calculate_budget_summary(monthly_income, items)

                # Render Metric Cards
                st.markdown("#### 📈 Financial Overview")
                mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                with mcol1:
                    render_metric_card(
                        "Monthly Income",
                        f"{CURRENCY_SYMBOL}{summary['income']:,.2f}",
                        "Total monthly inflow",
                        "#10B981"
                    )
                with mcol2:
                    render_metric_card(
                        "Total Expenses",
                        f"{CURRENCY_SYMBOL}{summary['total_expenses']:,.2f}",
                        f"{summary['item_count']} expense items",
                        "#3B82F6"
                    )
                with mcol3:
                    render_metric_card(
                        "Remaining Balance",
                        f"{CURRENCY_SYMBOL}{summary['remaining_balance']:,.2f}",
                        summary["health_status"],
                        summary["status_color"]
                    )
                with mcol4:
                    render_metric_card(
                        "Savings Rate",
                        f"{summary['savings_rate']:.1f}%",
                        "Target: >= 20%",
                        "#06B6D4" if summary["savings_rate"] >= 20 else "#F59E0B"
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                # Status Banner
                st.markdown(
                    f"""
                    <div style="background: rgba(15, 23, 42, 0.7); border-left: 4px solid {summary['status_color']};
                         padding: 0.9rem 1.2rem; border-radius: 8px; margin-bottom: 1.2rem;">
                        <span style="font-weight: 700; color: {summary['status_color']};">Status: {summary['health_status']}</span> —
                        <span style="color: #E2E8F0;">{summary['status_message']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Charts
                chart_tab1, chart_tab2 = st.tabs(["📊 Category Breakdown", "📋 Itemised Table"])

                with chart_tab1:
                    if summary["category_totals"]:
                        chart_df = pd.DataFrame([
                            {"Category": cat, "Amount": amt, "Percentage": summary["category_percentages"].get(cat, 0)}
                            for cat, amt in summary["category_totals"].items()
                        ]).sort_values(by="Amount", ascending=False)

                        chart = (
                            alt.Chart(chart_df)
                            .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
                            .encode(
                                x=alt.X("Amount:Q", title=f"Expense ({CURRENCY_SYMBOL})"),
                                y=alt.Y("Category:N", sort="-x", title="Category"),
                                color=alt.Color("Category:N", legend=None, scale=alt.Scale(scheme="tealblues")),
                                tooltip=["Category", "Amount", "Percentage"]
                            )
                            .properties(height=260)
                        )
                        st.altair_chart(chart, use_container_width=True)

                with chart_tab2:
                    items_df = pd.DataFrame(items)[["item", "category", "amount"]]
                    items_df.columns = ["Item Description", "Category", f"Amount ({CURRENCY_SYMBOL})"]
                    st.dataframe(items_df, use_container_width=True, height=220)

                # Gemini AI Advice Section
                st.markdown("---")
                st.markdown("#### 🤖 AI Saving Strategies & Budget Diagnostic")

                with st.spinner("Generating personalized AI financial strategies..."):
                    ai_result = analyze_budget_with_gemini(
                        monthly_income,
                        summary,
                        items,
                        api_key=st.session_state.user_api_key or None
                    )

                if ai_result["is_demo"]:
                    st.markdown(
                        f'<div class="glow-badge badge-demo">Source: {ai_result["source"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="glow-badge badge-live">Source: {ai_result["source"]}</div>',
                        unsafe_allow_html=True,
                    )

                with st.container(border=True):
                    st.markdown(ai_result["content"])

                # PDF Report Export
                st.markdown("#### 📄 Export Budget Report")
                pdf_data = generate_budget_pdf_report(summary, items, ai_result["content"])

                if pdf_data:
                    st.download_button(
                        label="📥 Download PDF Budget Report",
                        data=pdf_data,
                        file_name="PocketSmart_Budget_Report.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.info("PDF generation requires the `fpdf2` package. Install with `pip install fpdf2` to enable downloads.")
        else:
            st.info("👈 Enter your income and expenses on the left, then click **'⚡ Analyze My Budget'**.")


# =====================================================================
# TAB 2: AI EVENT COST ESTIMATOR
# =====================================================================

with tab_event:
    st.markdown("### 🎉 AI Event Cost & Budget Split Estimator")
    st.markdown(
        "Plan your event with precision. Get recommended percentage splits and exact amounts "
        "for Food, Venue, Decoration, Activities, and Miscellaneous."
    )

    ev_col1, ev_col2 = st.columns([1, 1.4])

    with ev_col1:
        st.markdown("#### 1. Event Parameters")
        event_type = st.selectbox(
            "Select Event Type",
            options=EVENT_TYPES,
            index=0,
            help="Choose the occasion type for tailored budget allocations.",
        )

        event_guests = st.number_input(
            "Expected Guest Count",
            min_value=1,
            max_value=10000,
            value=50,
            step=5,
            help="Total number of attendees expected.",
        )

        event_budget = st.number_input(
            f"Total Event Budget ({CURRENCY_SYMBOL})",
            min_value=500.0,
            max_value=10000000.0,
            value=30000.0,
            step=1000.0,
            format="%.2f",
            help="Maximum amount allocated for the event.",
        )

        event_preferences = st.text_area(
            "Special Preferences / Notes (Optional)",
            value="Outdoor evening event, vegetarian menu, photo booth, live acoustic music",
            height=100,
            placeholder="e.g. Traditional buffet, DJ requirements, theme colors...",
        )

        btn_estimate_event = st.button("🎉 Calculate Event Budget", use_container_width=True)

    with ev_col2:
        if btn_estimate_event or ("event_estimated" in st.session_state and st.session_state.event_estimated):
            st.session_state.event_estimated = True

            with st.spinner("Calculating event economics and AI recommendations..."):
                event_result = estimate_event_budget(
                    event_type,
                    event_guests,
                    event_budget,
                    event_preferences,
                    api_key=st.session_state.user_api_key or None
                )

            st.markdown("#### 📊 Budget Split & Economics")
            ev_m1, ev_m2, ev_m3 = st.columns(3)
            with ev_m1:
                render_metric_card(
                    "Total Budget",
                    f"{CURRENCY_SYMBOL}{event_budget:,.2f}",
                    event_type,
                    "#10B981"
                )
            with ev_m2:
                render_metric_card(
                    "Guest Count",
                    f"{event_guests}",
                    "Total Attendees",
                    "#3B82F6"
                )
            with ev_m3:
                render_metric_card(
                    "Cost Per Guest",
                    f"{CURRENCY_SYMBOL}{event_result['cost_per_guest']:,.2f}",
                    "Per-head expenditure",
                    "#06B6D4"
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Budget Split Dataframe & Chart
            split_df = pd.DataFrame(event_result["split_data"])
            split_df["Formatted_Amount"] = split_df["Amount"].apply(lambda x: f"{CURRENCY_SYMBOL}{x:,.2f}")
            split_df["Percentage_Str"] = split_df["Percentage"].apply(lambda x: f"{x}%")

            # Chart
            split_chart = (
                alt.Chart(split_df)
                .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
                .encode(
                    x=alt.X("Amount:Q", title=f"Allocated Amount ({CURRENCY_SYMBOL})"),
                    y=alt.Y("Category:N", sort="-x", title="Component"),
                    color=alt.Color("Category:N", legend=None, scale=alt.Scale(scheme="category10")),
                    tooltip=["Category", "Percentage_Str", "Formatted_Amount"]
                )
                .properties(height=200)
            )
            st.altair_chart(split_chart, use_container_width=True)

            # Table
            display_split_df = split_df[["Category", "Percentage_Str", "Formatted_Amount"]]
            display_split_df.columns = ["Component", "Allocation Share", f"Estimated Cost ({CURRENCY_SYMBOL})"]
            st.dataframe(display_split_df, use_container_width=True, hide_index=True)

            # AI Recommendations
            st.markdown("---")
            st.markdown("#### 💡 AI Event Strategy & Planning Advice")
            if event_result["is_demo"]:
                st.markdown(
                    f'<div class="glow-badge badge-demo">Source: {event_result["source"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="glow-badge badge-live">Source: {event_result["source"]}</div>',
                    unsafe_allow_html=True,
                )

            with st.container(border=True):
                st.markdown(event_result["recommendations"])
        else:
            st.info("👈 Set your event parameters and click **'🎉 Calculate Event Budget'** to see the detailed cost breakdown.")


# =====================================================================
# TAB 3: AI JEWELLERY MATCHER
# =====================================================================

with tab_jewellery:
    st.markdown("### 💎 AI Jewellery Matcher & Styling Consultant")
    st.markdown(
        "Upload a photo of your outfit or attire. Our AI examines the garment colors, neckline, "
        "and fabric aesthetic to suggest matching jewellery pieces within your defined budget."
    )

    st.markdown(
        """
        <div style="background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3B82F6;
             padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.82rem; color: #93C5FD;">
            🔒 <strong>Strict Privacy Guardrail:</strong> PocketSmart AI analyzes only clothing colors, neckline cut,
            and fabric styling. It does NOT identify individuals, faces, or biometric personal traits.
        </div>
        """,
        unsafe_allow_html=True,
    )

    jewel_col1, jewel_col2 = st.columns([1, 1.2])

    with jewel_col1:
        st.markdown("#### 1. Upload Outfit")
        uploaded_file = st.file_uploader(
            "Upload Outfit Image (JPG, JPEG, PNG)",
            type=SUPPORTED_IMAGE_FORMATS,
            help="Upload a clear photo of the dress, saree, suit, or attire you plan to wear.",
        )

        pil_image = None
        if uploaded_file is not None:
            try:
                pil_image = Image.open(uploaded_file)
                st.image(pil_image, caption="Uploaded Outfit Preview", use_container_width=True)
            except Exception as e:
                st.error(f"Could not open uploaded image: {str(e)}")

        st.markdown("#### 2. Styling Preferences")
        jewellery_budget = st.number_input(
            f"Jewellery Budget ({CURRENCY_SYMBOL})",
            min_value=500.0,
            max_value=1000000.0,
            value=6000.0,
            step=500.0,
            format="%.2f",
            help="Total spending limit for jewellery accessories.",
        )

        jewellery_style = st.selectbox(
            "Preferred Jewellery Style",
            options=JEWELLERY_STYLES,
            index=0,
            help="Select the design aesthetic that matches your taste.",
        )

        btn_match_jewellery = st.button("💎 Find Matching Jewellery", use_container_width=True)

    with jewel_col2:
        if btn_match_jewellery or ("jewellery_matched" in st.session_state and st.session_state.jewellery_matched):
            st.session_state.jewellery_matched = True

            with st.spinner("Stylist AI is analyzing outfit aesthetics and matching jewellery..."):
                jewel_result = recommend_jewellery(
                    pil_image,
                    jewellery_budget,
                    jewellery_style,
                    api_key=st.session_state.user_api_key or None
                )

            st.markdown("#### 👑 Recommended Jewellery Lookbook")
            if jewel_result["is_demo"]:
                st.markdown(
                    f'<div class="glow-badge badge-demo">Source: {jewel_result["source"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="glow-badge badge-live">Source: {jewel_result["source"]}</div>',
                    unsafe_allow_html=True,
                )

            with st.container(border=True):
                st.markdown(jewel_result["content"])
        else:
            st.info("👈 Upload an outfit image or select your style preferences, then click **'💎 Find Matching Jewellery'**.")


# =====================================================================
# FOOTER
# =====================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
foot_col1, foot_col2 = st.columns([2, 1])
with foot_col1:
    st.caption(f"© PocketSmart AI — {APP_SUBTITLE}")
    st.caption(FINANCIAL_DISCLAIMER)
with foot_col2:
    st.caption(f"Powered by Streamlit & Google Gemini ({GEMINI_MODEL})")
