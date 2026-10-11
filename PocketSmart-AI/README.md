# 💰 PocketSmart AI
> *"Your Smart Budget & Recommendation Assistant"*

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-4285F4?style=flat&logo=google&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

PocketSmart AI is an intelligent personal finance and event recommendation assistant built using Python, Streamlit, and Google Gemini Generative AI. It features an aesthetic dark "glow" themed dashboard designed to empower users to manage expenses, optimize event budgets, and match jewellery with outfits—with zero hassle and full fallback safety.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Project Structure](#-project-structure)
5. [Prerequisites & Requirements](#-prerequisites--requirements)
6. [Step-by-Step Installation](#-step-by-step-installation)
7. [Environment & Gemini Configuration](#-environment--gemini-configuration)
8. [Running the Application](#-running-the-application)
9. [Safe Demo / Fallback Mode](#-safe-demo--fallback-mode)
10. [Testing Checklist](#-testing-checklist)
11. [Troubleshooting](#-troubleshooting)
12. [Security & Privacy Practices](#-security--privacy-practices)
13. [Deployment Guide](#-deployment-guide)
14. [Disclaimer](#-disclaimer)

---

## 🌟 Project Overview

Managing personal finances, budgeting for social functions, and making smart accessory choices often involves fragmented tools and guesswork. **PocketSmart AI** unifies these tasks in an interactive, visually stunning dashboard. It pairs local computational rule engines with Google Gemini's multimodal reasoning to provide instant, actionable insights.

---

## 🚀 Key Features

### 1. 📊 Smart Budget Analyzer
- **Flexible Expense Parsing:** Accepts diverse expense text syntaxes such as:
  ```text
  Food 250
  Transport: 120
  Electricity - 900
  Shopping = 600
  Rent 8000
  ```
- **Automated Categorization:** Classifies inputs into predefined categories: *Food, Transport, Utilities, Shopping, Housing, Education, Entertainment, Health, and Other*.
- **Financial Metrics & Visualizations:** Computes total expenses, remaining balance, savings rate (%), and interactive bar/distribution charts.
- **AI-Powered Financial Strategy:** Connects to Google Gemini to deliver a 4-part financial health diagnostic, spending leak analysis, cost-cutting plan, and a 30-day budget challenge.
- **PDF Export:** Generates an executive PDF report containing metrics, breakdowns, and AI recommendations.

### 2. 🎉 AI Event Cost Estimator
- **Occasion-Specific Budget Splits:** Tailored allocations for *Birthday Parties, College Events, Family Functions, and Custom Gatherings*.
- **Multi-Category Allocation:** Allocates funds across *Food, Venue, Decoration, Activities, and Miscellaneous*.
- **Dual Representation:** Displays both exact percentages (%) and calculated Rupee amounts (₹).
- **Per-Guest Economics:** Calculates exact per-head costs and delivers AI vendor negotiation strategies.

### 3. 💎 AI Jewellery Matcher
- **Multimodal Fashion Vision:** Upload photos of your outfit (JPG, JPEG, PNG).
- **Style Customization:** Match against styles including *Minimal, Traditional, Modern, Party Wear, or Any*.
- **Budget-Conscious Allocation:** Breaks down an accessory budget across Neckwear, Earrings, Bangles/Bracelets, and Rings.
- **Strict Privacy Safeguard:** Focuses solely on garment colors, textures, and neckline cuts without identifying faces or individuals.

---

## 🏛️ System Architecture

```text
User Input (Text / Image / Numbers)
              ↓
 Streamlit Frontend (Tabs, Glow UI, Forms)
              ↓
 Python Backend (Parsing, Validation, Calculations)
              ↓
 Google Gemini Generative AI (NLP & Vision)
    [or Fallback Deterministic Engine if Offline]
              ↓
 AI Diagnostics, Strategy & Budget Splits
              ↓
 Visual Charts, Metric Cards, Downloadable PDF
```

---

## 📂 Project Structure

```text
PocketSmart-AI/
│
├── app.py                  # Main Streamlit dashboard application
├── style.py                # Dark glow CSS styling & metric card renderers
├── requirements.txt        # Python dependency manifest
├── README.md               # Complete project documentation
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules for virtual environments and secrets
├── run_windows.bat         # 1-click Windows launcher
│
├── src/
│   ├── __init__.py         # Package initializer
│   ├── ai_engine.py        # Gemini client, prompts, and demo fallback rules
│   └── utils.py            # Expense parsing, category matching, masking, and PDF generation
│
├── config/
│   ├── __init__.py         # Package initializer
│   └── settings.py         # Application constants, models, and keyword mappings
│
└── static/
    └── README.txt          # Static media assets documentation
```

---

## 💻 Prerequisites & Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **Python Version:** Python 3.9, 3.10, 3.11, or 3.12
- **VS Code:** Recommended editor (with Python extension)
- **Google Gemini API Key:** Optional (for Live AI mode; Demo mode works without any key)

---

## 🛠️ Step-by-Step Installation

### Step 1: Clone or Open the Repository in VS Code
Open VS Code, select **File > Open Folder...**, and select the `PocketSmart-AI` directory.

### Step 2: Create a Virtual Environment
Open the integrated terminal in VS Code (`Ctrl + ~`) and run:

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

**On Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

> **PowerShell Execution Policy Note:**
> If you encounter an execution policy error such as `cannot be loaded because running scripts is disabled on this system`, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .venv\Scripts\activate
> ```
> Alternatively, switch to **Command Prompt (CMD)** in VS Code and run:
> ```cmd
> .venv\Scripts\activate.bat
> ```

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies
Ensure `pip` is up to date, then install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 🔑 Environment & Gemini Configuration

1. Copy the `.env.example` file to create your local `.env`:
   ```bash
   copy .env.example .env
   ```
   *(On macOS/Linux: `cp .env.example .env`)*

2. Open `.env` in VS Code and insert your Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
   GEMINI_MODEL=gemini-1.5-flash
   ```

3. To obtain a free Gemini API key:
   - Visit [Google AI Studio](https://aistudio.google.com/).
   - Sign in with your Google account.
   - Click **Get API key** and create a new project key.

> **Note:** You can also enter or override your Gemini API key directly from the application's sidebar without restarting the server!

---

## 🏃 Running the Application

### Method 1: Using the Terminal
With the virtual environment activated, run:

```bash
python -m streamlit run app.py
```

### Method 2: 1-Click Windows Launcher
Double-click `run_windows.bat` in the project root directory.

### Expected Local URL:
```text
http://localhost:8501
```
The application will automatically launch in your default web browser.

---

## 🛡️ Safe Demo / Fallback Mode

PocketSmart AI includes **zero-crash fallback resilience**:
- If `GEMINI_API_KEY` is missing or invalid,
- If internet connectivity drops or Gemini servers return a 429/quota error,
- Or if the `google-generativeai` package is uninstalled,

The application **will not crash**. It displays a clear `🟡 Demo Fallback Mode` indicator and seamlessly activates the local deterministic rule engine. All calculations, budget splits, saving analyses, and jewellery advice continue to function accurately.

---

## 🧪 Testing Checklist

Use these test cases to verify full functionality:

| Test Case | Description | Action | Expected Result |
| :--- | :--- | :--- | :--- |
| **TC-01** | Multi-format expense parsing | Paste 5 lines: `Food 250`, `Transport: 120`, `Electricity - 900`, `Shopping = 600`, `Rent 8000` | Successfully parsed, categorized, and displayed in charts. |
| **TC-02** | Budget balance calculation | Enter Income: ₹25,000 with total expenses ₹9,870 | Remaining balance shows ₹15,130, savings rate shows ~60.5%, status shows Healthy. |
| **TC-03** | Event Cost Estimator | Select *Birthday Party*, Guests: 50, Budget: ₹30,000 | Correct 5-way split (Food 40%, Venue 25%, etc.) with per-head cost of ₹600. |
| **TC-04** | AI Jewellery Matcher | Upload a JPG/PNG outfit, set budget ₹5,000, style *Minimal* | Generates tailored jewellery recommendations and 4-tier budget split. |
| **TC-05** | Missing API key (Demo Mode) | Clear the API key in `.env` and restart | App starts smoothly, shows "Demo Fallback Mode" badge, and generates offline advice. |
| **TC-06** | Invalid / Malformed Input | Enter non-numeric lines: `Rent Free`, `-500 Food` | Friendly warning messages appear; valid lines are preserved without crashing. |
| **TC-07** | Invalid Gemini Model | Set `GEMINI_MODEL=invalid-model` in `.env` | Catches model error gracefully and switches to deterministic recommendations. |
| **TC-08** | PDF Report Download | Click "📥 Download PDF Budget Report" | Generates and downloads a clean, printable PDF report. |

---

## 🔧 Troubleshooting

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| `streamlit: command not found` | Virtual environment not activated | Run `.venv\Scripts\activate` or execute using `python -m streamlit run app.py`. |
| `Script execution disabled` (PowerShell) | Execution Policy restricted | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell. |
| `ModuleNotFoundError: No module named 'fpdf'` | Missing fpdf2 | Run `python -m pip install fpdf2`. |
| `API_KEY_INVALID` or `404 Model Not Found` | Typo in API key or outdated model | Verify key in `.env` or paste it directly in the app's sidebar. Ensure `GEMINI_MODEL=gemini-1.5-flash`. |
| Image upload fails | File format not supported | Upload files with `.jpg`, `.jpeg`, or `.png` extensions. |

---

## 🔒 Security & Privacy Practices

1. **Secret Isolation:** `.env` and `.streamlit/secrets.toml` are strictly listed in `.gitignore`. **NEVER** push these files to public repositories.
2. **Sensitive Data Masking:** All user inputs are sanitized with `mask_sensitive_data()` before transmission to Gemini, replacing credit card numbers, phone numbers, and account identifiers with safe tokens.
3. **Biometric & Facial Privacy:** In the AI Jewellery Matcher, strict prompts prohibit the model from identifying faces, gender, ethnicity, or personal identities.
4. **No Secret Leaks:** API keys and credentials are never exposed in user error banners or logs.

---

## 🚢 Deployment Guide

### A. Deploy to Streamlit Community Cloud (Recommended)
1. Push your repository to GitHub (**ensure `.env` is NOT committed**).
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Select your repository, branch (`main`), and entry point (`app.py`).
4. In **Advanced Settings > Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   GEMINI_MODEL = "gemini-1.5-flash"
   ```
5. Click **Deploy!**

### B. Deploy via Google Cloud Run / Docker
Create a `Dockerfile` in the root:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Deploy using Google Cloud SDK:
```bash
gcloud run deploy pocketsmart-ai --source . --platform managed --allow-unauthenticated
```
Inject environment variables using `--set-env-vars GEMINI_API_KEY=your_key`.

---

## ⚖️ Disclaimer

> **Educational Guidance Notice:**
> PocketSmart AI provides educational budgeting guidance and algorithmic recommendations. It is **not** a substitute for certified professional financial advice, tax counseling, or legal planning.
