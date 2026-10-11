"""
PocketSmart AI - AI Engine
Integrates Google Gemini AI for Smart Budget Analysis, Event Cost Estimation,
and Vision-based Jewellery Recommendations.
Includes dual SDK/HTTPS transport, error handling, privacy guardrails, and deterministic Demo Fallbacks.
"""

import os
import base64
import io
from typing import Dict, Any, List, Optional, Tuple
from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    CURRENCY_SYMBOL,
    FINANCIAL_DISCLAIMER,
    EVENT_BASELINE_SPLITS,
    is_gemini_configured,
)
from src.utils import mask_sensitive_data

# Safe import of Google Generative AI SDK
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except Exception:
    genai = None
    GENAI_AVAILABLE = False

# Safe import of requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except Exception:
    requests = None
    REQUESTS_AVAILABLE = False


# =====================================================================
# GEMINI MODEL CONFIGURATION & TRANSPORT
# =====================================================================

def configure_gemini(api_key: Optional[str] = None) -> tuple:
    """
    Checks if a valid Gemini API key is configured.
    Returns (model_instance, is_configured, status_message).
    """
    active_key = (api_key or GEMINI_API_KEY or "").strip()

    if not active_key or active_key == "your_api_key_here":
        return None, False, "Gemini API key is not configured. Operating in Demo Fallback Mode."

    return None, True, f"Connected to Gemini ({GEMINI_MODEL})"


def _call_gemini_api(
    prompt: str,
    image: Any = None,
    api_key: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Dispatches generation request to Gemini.
    Attempts Google Generative AI SDK first; if blocked by environment/DLL policies,
    transparently falls back to direct HTTPS REST API (via requests).
    Returns (response_text, error_message).
    """
    active_key = (api_key or GEMINI_API_KEY or "").strip()
    if not active_key or active_key == "your_api_key_here":
        return None, "Gemini API key is not configured."

    # 1. Try SDK if available and not blocked
    if GENAI_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=active_key)
            model = genai.GenerativeModel(GEMINI_MODEL)
            if image is not None:
                resp = model.generate_content([prompt, image])
            else:
                resp = model.generate_content(prompt)
            if resp and resp.text:
                return resp.text.strip(), None
        except Exception:
            pass  # Fall through to HTTPS REST fallback

    # 2. Direct HTTPS REST API
    if REQUESTS_AVAILABLE and requests is not None:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={active_key}"
        parts = [{"text": prompt}]

        if image is not None:
            try:
                buf = io.BytesIO()
                rgb_img = image.convert("RGB") if hasattr(image, "convert") else image
                rgb_img.save(buf, format="JPEG")
                img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_b64
                    }
                })
            except Exception:
                pass

        payload = {"contents": [{"parts": parts}]}
        try:
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=payload, headers=headers, timeout=25)
            if r.status_code == 200:
                data = r.json()
                candidates = data.get("candidates", [])
                if candidates:
                    content_parts = candidates[0].get("content", {}).get("parts", [])
                    if content_parts and "text" in content_parts[0]:
                        return content_parts[0]["text"].strip(), None
                return None, "No text candidates returned by Gemini."
            else:
                err_body = r.json().get("error", {}).get("message", r.text[:80])
                return None, f"HTTP {r.status_code}: {err_body}"
        except Exception as ex:
            return None, f"Network error: {str(ex)}"

    return None, "No available HTTP/SDK transport to reach Gemini."


# =====================================================================
# 1. SMART BUDGET ANALYZER
# =====================================================================

def analyze_budget_with_gemini(
    income: float,
    summary: Dict[str, Any],
    items: List[Dict[str, Any]],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes user expenses using Gemini AI, or generates structured
    deterministic recommendations if in Demo Mode.
    """
    cat_breakdown_str = "\n".join(
        [f"- {cat}: {CURRENCY_SYMBOL}{amt:,.2f} ({summary['category_percentages'].get(cat, 0):.1f}%)"
         for cat, amt in summary["category_totals"].items()]
    )

    item_sample = ", ".join([mask_sensitive_data(it["item"]) for it in items[:15]])

    prompt = f"""
You are a certified, friendly personal finance advisor assisting a user with their monthly budget.
Analyze the following financial snapshot:

Monthly Income: {CURRENCY_SYMBOL}{income:,.2f}
Total Expenses: {CURRENCY_SYMBOL}{summary['total_expenses']:,.2f}
Remaining Balance: {CURRENCY_SYMBOL}{summary['remaining_balance']:,.2f}
Savings Rate: {summary['savings_rate']:.1f}%

Category Breakdown:
{cat_breakdown_str}

Sample Items logged: {item_sample}

Rules:
1. Provide realistic, educational budgeting guidance.
2. DO NOT invent or assume fake transactions not mentioned above.
3. Compare spending against the 50/30/20 rule (Needs/Wants/Savings).
4. Provide exactly these 4 clear sections formatted in Markdown:
   ### 1. Financial Health Diagnostic
   ### 2. Top Spending Leaks & Observations
   ### 3. Tailored Saving Strategies (3-4 high-impact, actionable steps)
   ### 4. 30-Day Budget Challenge

Keep the tone encouraging, structured, and practical.
"""

    gemini_text, err = _call_gemini_api(prompt, api_key=api_key)

    if gemini_text:
        full_text = gemini_text + f"\n\n---\n*Disclaimer: {FINANCIAL_DISCLAIMER}*"
        return {
            "success": True,
            "is_demo": False,
            "content": full_text,
            "source": f"Google Gemini ({GEMINI_MODEL})"
        }

    # FALLBACK / DEMO STRATEGY
    fallback_text = _generate_fallback_budget_advice(income, summary)
    note = err or "Operating in Demo Fallback Mode"
    return {
        "success": True,
        "is_demo": True,
        "content": fallback_text,
        "source": f"PocketSmart Rule Engine ({note})"
    }


def _generate_fallback_budget_advice(income: float, summary: Dict[str, Any]) -> str:
    """Generates dynamic rule-based saving strategies when Gemini is unavailable."""
    balance = summary["remaining_balance"]
    rate = summary["savings_rate"]
    top_categories = sorted(
        summary["category_totals"].items(), key=lambda x: x[1], reverse=True
    )
    top_cat_name, top_cat_amt = top_categories[0] if top_categories else ("General", 0)

    advice = f"""
### 1. Financial Health Diagnostic (Demo Mode)
- **Income Utilization:** You are currently spending **{(100 - rate) if income > 0 else 100:.1f}%** of your monthly income.
- **Top Spend Driver:** Your largest expenditure is **{top_cat_name}** at **{CURRENCY_SYMBOL}{top_cat_amt:,.2f}** ({summary['category_percentages'].get(top_cat_name, 0):.1f}% of total outflow).
- **50/30/20 Assessment:** {"Your savings rate exceeds the 20% benchmark. Outstanding discipline!" if rate >= 20 else "Your savings rate is under 20%. Reallocating 5-10% from discretionary spending into an emergency buffer will build solid financial resilience."}

### 2. Top Spending Leaks & Observations
- **High Concentration:** {top_cat_name} accounts for a major chunk of your budget. Even a 10% trim here can save **{CURRENCY_SYMBOL}{round(top_cat_amt * 0.1, 2):,.2f}** monthly.
- **Balance Position:** {"You have a surplus of " + CURRENCY_SYMBOL + f"{balance:,.2f}. Consider automated transfers to high-yield savings or mutual funds." if balance > 0 else "You are in a deficit of " + CURRENCY_SYMBOL + f"{abs(balance):,.2f}. Discretionary categories like Entertainment and Shopping require immediate caps."}

### 3. Tailored Saving Strategies
1. **The 10% Quick Win on {top_cat_name}:** Review your frequent receipts in {top_cat_name}. Audit recurring subscriptions and opt for bulk purchases or cook-at-home alternatives.
2. **The 72-Hour Rule for Shopping:** Before buying non-essential items, wait 72 hours. This eliminates over 60% of impulse purchases.
3. **Automate Pay-Yourself-First:** Automatically route at least 15% of your income into a separate savings account the day your salary arrives.
4. **Utility & Plan Optimization:** Review broadband, electricity peak loads, and mobile tariffs. Small recurring optimizations yield substantial annual savings.

### 4. 30-Day Budget Challenge
- **Week 1:** Track daily coffee, snacking, and micro-transit spends.
- **Week 2:** Implement one "No-Spend Day" per week.
- **Week 3:** Cancel at least one unused recurring digital subscription.
- **Week 4:** Bank all accumulated savings into an emergency fund.

---
*Disclaimer: {FINANCIAL_DISCLAIMER}*
"""
    return advice.strip()


# =====================================================================
# 2. AI EVENT COST ESTIMATOR
# =====================================================================

def estimate_event_budget(
    event_type: str,
    guests: int,
    total_budget: float,
    preferences: str = "",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Estimates event budget allocation across Food, Venue, Decoration,
    Activities, and Miscellaneous with amounts and percentages.
    """
    baseline_split = EVENT_BASELINE_SPLITS.get(
        event_type, EVENT_BASELINE_SPLITS["Other"]
    )

    split_data = []
    for cat, pct in baseline_split.items():
        allocated_amt = round((pct / 100.0) * total_budget, 2)
        split_data.append({
            "Category": cat,
            "Percentage": pct,
            "Amount": allocated_amt
        })

    cost_per_guest = round(total_budget / guests, 2) if guests > 0 else 0.0

    pref_cleaned = mask_sensitive_data(preferences)
    prompt = f"""
You are an expert event planner. Help optimize a budget for an upcoming event:

- Event Type: {event_type}
- Guest Count: {guests} attendees
- Total Budget: {CURRENCY_SYMBOL}{total_budget:,.2f}
- Estimated Cost Per Guest: {CURRENCY_SYMBOL}{cost_per_guest:,.2f}
- Specific Preferences/Requirements: {pref_cleaned or "Standard arrangements"}

The standard recommended allocation is:
{baseline_split}

Provide an event planning analysis in Markdown with:
### 1. Per-Head Economics & Feasibility
### 2. Smart Cost-Optimization Tactics (Category by Category)
### 3. Vendor Negotiation & Checklist
### 4. Contingency Buffer Strategy

Keep it realistic, practical, and tailored to the budget of {CURRENCY_SYMBOL}{total_budget:,.2f}.
"""
    gemini_text, err = _call_gemini_api(prompt, api_key=api_key)

    if gemini_text:
        full_text = gemini_text + f"\n\n---\n*Disclaimer: {FINANCIAL_DISCLAIMER}*"
        return {
            "split_data": split_data,
            "cost_per_guest": cost_per_guest,
            "recommendations": full_text,
            "is_demo": False,
            "source": f"Google Gemini ({GEMINI_MODEL})"
        }

    # Fallback recommendations
    fallback_text = f"""
### 1. Per-Head Economics & Feasibility (Demo Mode)
- **Allocated Spend per Guest:** **{CURRENCY_SYMBOL}{cost_per_guest:,.2f}** across all expenses.
- **Feasibility:** For a **{event_type}** with **{guests} guests**, this budget is {"well-proportioned" if cost_per_guest >= 500 else "tight, requiring careful venue and catering negotiations"}.

### 2. Smart Cost-Optimization Tactics
- **Food & Catering ({baseline_split.get('Food', 35)}%):** Limit menu items to 2 appetizers, 1 main course, and 1 dessert. Buffets save 25% compared to plated service.
- **Venue ({baseline_split.get('Venue', 25)}%):** Consider clubhouses, community halls, or outdoor lawns to reduce hourly rental fees.
- **Decorations ({baseline_split.get('Decoration', 15)}%):** Use fairy lights, reusable signage, and balloon arches rather than fresh exotic flowers.
- **Activities & Music ({baseline_split.get('Activities', 15)}%):** Create a curated Spotify playlist and host interactive group games rather than hiring an external DJ.

### 3. Contingency & Vendor Checklist
- Always maintain **10% Miscellaneous ({CURRENCY_SYMBOL}{round(total_budget * 0.1, 2):,.2f})** for last-minute tips, extra servings, or generator backups.
- Confirm vendor arrival times 48 hours prior.

---
*Disclaimer: {FINANCIAL_DISCLAIMER}*
"""
    return {
        "split_data": split_data,
        "cost_per_guest": cost_per_guest,
        "recommendations": fallback_text.strip(),
        "is_demo": True,
        "source": "PocketSmart Rule Engine (Demo Mode)"
    }


# =====================================================================
# 3. AI JEWELLERY MATCHER
# =====================================================================

def recommend_jewellery(
    image: Any,
    budget: float,
    style: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes an uploaded outfit image using Gemini Vision capabilities
    to recommend matching jewellery based on style and budget.
    Ensures strict privacy: does not identify person or personal traits.
    """
    prompt = f"""
You are a celebrity fashion stylist and jewellery design consultant.
Analyze the clothing and outfit shown in the image to recommend matching jewellery.

STRICT PRIVACY GUARDRAILS:
- Focus solely on the clothing colors, neckline, fabric texture, pattern, and aesthetic.
- DO NOT identify the person, facial features, age, gender, ethnicity, or biometric attributes.
- DO NOT infer sensitive personal traits.

User Preferences:
- Budget Limit: {CURRENCY_SYMBOL}{budget:,.2f}
- Preferred Jewellery Style: {style}

Provide your structured recommendations in Markdown:
### 1. Outfit Aesthetic & Color Harmony
### 2. Recommended Jewellery Pieces (Necklace, Earrings, Bangles/Bracelet, Ring)
### 3. Metal & Stone Suggestions (Gold, Silver, Rose Gold, Kundan, Pearls, etc.)
### 4. Smart Budget Breakdown (Allocating {CURRENCY_SYMBOL}{budget:,.2f})
### 5. Pro Styling Tip for this Look
"""
    gemini_text, err = _call_gemini_api(prompt, image=image, api_key=api_key)

    if gemini_text:
        full_text = gemini_text + f"\n\n---\n*Disclaimer: {FINANCIAL_DISCLAIMER}*"
        return {
            "success": True,
            "is_demo": False,
            "content": full_text,
            "source": f"Google Gemini Vision ({GEMINI_MODEL})"
        }

    # Deterministic Fallback Recommendation
    fallback_text = _generate_fallback_jewellery_advice(budget, style)
    return {
        "success": True,
        "is_demo": True,
        "content": fallback_text,
        "source": "PocketSmart Fashion Advisor (Demo Mode)"
    }


def _generate_fallback_jewellery_advice(budget: float, style: str) -> str:
    """Generates structured jewellery suggestions tailored to the chosen style and budget."""
    neck_share = round(budget * 0.45, 2)
    ear_share = round(budget * 0.30, 2)
    wrist_share = round(budget * 0.15, 2)
    ring_share = round(budget * 0.10, 2)

    style_guide = {
        "Minimal": {
            "metal": "Dainty 18K Yellow Gold or Rhodium-plated Sterling Silver",
            "pieces": "Sleek pendant chain, subtle cubic zirconia studs, and a slim geometric cuff.",
            "tip": "Focus on clean lines. A single delicate focal point elevates minimalist outfits effortlessly."
        },
        "Traditional": {
            "metal": "Matte Gold, Temple Jewellery, or Polki & Kundan work with Pearl drops",
            "pieces": "Choker or layered Rani Haar, statement Jhumkas, and intricate Kada bangles.",
            "tip": "Match the metal warmth with your outfit's zari or embroidery undertone."
        },
        "Modern": {
            "metal": "Rose Gold, Platinum finish, or Sculptural contemporary Brass",
            "pieces": "Asymmetrical hoop earrings, paperclip chain link necklace, and stackable bands.",
            "tip": "Mix textures—pair polished metallic finishes with matte fabrics for contrast."
        },
        "Party Wear": {
            "metal": "Rhodium silver, Crystal / American Diamond, or Oxidised Silver with colored gems",
            "pieces": "Sparkling chandelier earrings, tennis bracelet, and an eye-catching cocktail ring.",
            "tip": "If the outfit has heavy sequins or a high collar, skip the heavy necklace and let statement earrings take center stage."
        },
        "Any": {
            "metal": "Versatile Sterling Silver or Classic Gold-tone with freshwater pearls",
            "pieces": "Convertible drop earrings, layered chain with dainty medallion, and pearl bracelet.",
            "tip": "Select pieces that transition seamlessly between daytime and evening lighting."
        }
    }

    info = style_guide.get(style, style_guide["Any"])

    return f"""
### 1. Outfit Aesthetic & Color Harmony (Demo Mode)
- **Style Archetype:** **{style} Collection**
- **Recommended Finish:** {info['metal']}
- **Design Philosophy:** Harmonizes with both solid tones and textured fabrics, maintaining visual balance without overpowering the garment.

### 2. Recommended Jewellery Pieces
- **Neckwear:** {info['pieces'].split(',')[0] if ',' in info['pieces'] else 'Refined necklace accent'}
- **Earrings:** {info['pieces'].split(',')[1] if ',' in info['pieces'] and len(info['pieces'].split(',')) > 1 else 'Matching studs or drops'}
- **Wrists & Hands:** {info['pieces'].split(',')[2] if ',' in info['pieces'] and len(info['pieces'].split(',')) > 2 else 'Subtle accent band'}

### 3. Suggested Budget Allocation ({CURRENCY_SYMBOL}{budget:,.2f})
- **Statement Piece / Necklace (45%):** {CURRENCY_SYMBOL}{neck_share:,.2f}
- **Earrings / Studs (30%):** {CURRENCY_SYMBOL}{ear_share:,.2f}
- **Bangles / Bracelet (15%):** {CURRENCY_SYMBOL}{wrist_share:,.2f}
- **Ring / Accents (10%):** {CURRENCY_SYMBOL}{ring_share:,.2f}

### 4. Pro Styling Tip
💡 {info['tip']}

---
*Disclaimer: {FINANCIAL_DISCLAIMER}*
""".strip()
