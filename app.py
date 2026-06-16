import pandas as pd
from flask import Flask, render_template, request, send_file,redirect
import joblib
import os
import sqlite3
import re

from dotenv import load_dotenv
import google.generativeai as genai

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# =====================================
# Flask App
# =====================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# =====================================
# Load ML Model
# =====================================

model = joblib.load(
    "models/phishing_model.pkl"
)

vectorizer = joblib.load(
    "models/vectorizer.pkl"
)

# =====================================
# Home Route
# =====================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# =====================================
# Dashboard Route
# =====================================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(
        "database/phishing.db"
    )

    cursor = conn.cursor()

    # ==========================
    # Total Analyses
    # ==========================

    cursor.execute(
        "SELECT COUNT(*) FROM analysis_history"
    )

    total = cursor.fetchone()[0]

    # ==========================
    # Phishing Count
    # ==========================

    cursor.execute("""
    SELECT COUNT(*)
    FROM analysis_history
    WHERE prediction='PHISHING EMAIL'
    """)

    phishing = cursor.fetchone()[0]

    safe = total - phishing

    # ==========================
    # Percentages
    # ==========================

    if total > 0:

        phishing_percent = round(
            (phishing / total) * 100,
            1
        )

        safe_percent = round(
            (safe / total) * 100,
            1
        )

    else:

        phishing_percent = 0
        safe_percent = 0

    # ==========================
    # Risk Distribution
    # ==========================

    cursor.execute("""
    SELECT COUNT(*)
    FROM analysis_history
    WHERE risk_level='Critical'
    """)

    critical_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM analysis_history
    WHERE risk_level='High'
    """)

    high_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM analysis_history
    WHERE risk_level='Medium'
    """)

    medium_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM analysis_history
    WHERE risk_level='Low'
    """)

    low_count = cursor.fetchone()[0]

    # ==========================
    # Recent History
    # ==========================

    cursor.execute("""
    SELECT
        prediction,
        confidence,
        risk_score,
        risk_level,
        created_at

    FROM analysis_history

    ORDER BY id DESC

    LIMIT 10
    """)

    history = cursor.fetchall()

    conn.close()

    # ==========================
    # Render Dashboard
    # ==========================

    return render_template(
        "dashboard.html",

        total=total,

        phishing=phishing,
        safe=safe,

        phishing_percent=phishing_percent,
        safe_percent=safe_percent,

        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,

        history=history
    )

@app.route("/export_csv")
def export_csv():

    conn = sqlite3.connect(
        "database/phishing.db"
    )

    query = """
    SELECT *
    FROM analysis_history
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    filename = (
        f"reports/analysis_history_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    df.to_csv(
        filename,
        index=False
    )

    return send_file(
        filename,
        as_attachment=True
    )
# =====================================
# PDF Report Route
# =====================================

@app.route("/generate_report")
def generate_report():

    conn = sqlite3.connect(
        "database/phishing.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        prediction,
        confidence,
        risk_score,
        risk_level,
        threats,
        analysis,
        created_at
    FROM analysis_history
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if not row:
        return "No report data found."

    prediction = row[0]
    confidence = row[1]
    risk_score = row[2]
    risk_level = row[3]
    threats = row[4]
    analysis = row[5]
    created_at = row[6]

    filename = (
        f"reports/report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Phishing Detection Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Prediction: {prediction}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Confidence: {confidence:.2f}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Score: {risk_score}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {risk_level}",
            styles["Normal"]
        )
    )

    content.append(
    Paragraph(
        "Threat Indicators",
        styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            str(threats) if threats else "No threat indicators found.",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "AI Security Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            str(analysis) if analysis else "No AI analysis available.",
            styles["Normal"]
        )
    )
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Generated: {created_at}",
            styles["Normal"]
        )
    )
    doc.build(content)

    return send_file(
        filename,
        as_attachment=True
    )

@app.route("/clear_history")
def clear_history():

    conn = sqlite3.connect(
        "database/phishing.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM analysis_history"
    )

    conn.commit()

    conn.close()

    return redirect("/dashboard")
# =====================================
# Prediction Route
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    email_text = request.form.get(
        "email",
        ""
    )

    uploaded_file = request.files.get(
        "email_file"
    )

    if uploaded_file and uploaded_file.filename:

        email_text = uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

    # Empty input check

    if not email_text.strip():

        return render_template(
            "index.html",
            prediction="Please enter or upload an email."
        )
    # =================================
    # ML Prediction
    # =================================

    email_vector = vectorizer.transform(
        [email_text]
    )

    prediction = model.predict(
        email_vector
    )[0]

    probabilities = model.predict_proba(
        email_vector
    )[0]

    safe_probability = (
        probabilities[0] * 100
    )

    phishing_probability = (
        probabilities[1] * 100
    )

    # =================================
    # Result
    # =================================

    if prediction == 1:

        result = "PHISHING EMAIL"

        confidence = phishing_probability

        result_class = "danger"

    else:

        result = "SAFE EMAIL"

        confidence = safe_probability

        result_class = "safe"

    # =================================
    # Risk Score
    # =================================

    risk_score = int(
        phishing_probability
    )

    if risk_score <= 25:

        risk_level = "Low"

    elif risk_score <= 50:

        risk_level = "Medium"

    elif risk_score <= 75:

        risk_level = "High"

    else:

        risk_level = "Critical"

    # =================================
    # Threat Indicators
    # =================================

    threats = []

    email_lower = email_text.lower()

    keyword_mapping = {

        "urgent":
        "Urgency Language",

        "verify":
        "Verification Request",

        "password":
        "Credential Request",

        "login":
        "Login Request",

        "click":
        "Suspicious Call-To-Action",

        "bank":
        "Financial Targeting",

        "account":
        "Account Threat",

        "suspended":
        "Account Suspension Tactic",

        "security":
        "Security Alert",

        "update":
        "Update Request"
    }

    for keyword, threat in keyword_mapping.items():

        if keyword in email_lower:

            threats.append(
                threat
            )
    # ==========================
# URL Extraction
# ==========================

    url_pattern = r'https?://[^\s]+'

    urls_found = re.findall(
        url_pattern,
        email_text
    )
    if len(urls_found) > 0:

        threats.append(
            f"URLs Detected ({len(urls_found)})"
    )
    # =================================
    # Gemini Analysis
    # =================================

    analysis = ""

    try:

        prompt = f"""
You are a professional cybersecurity analyst.

Analyze the email below.

EMAIL:
{email_text}

Return:

Threat Summary

Attack Type

Risk Assessment

Recommendations

Keep response under 120 words.
"""

        response = (
            gemini_model.generate_content(
                prompt
            )
        )

        analysis = response.text

    except Exception as e:

        analysis = (
            f"AI Analysis unavailable: {str(e)}"
        )

    # =================================
    # Save To SQLite
    # =================================

    conn = sqlite3.connect(
        "database/phishing.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
INSERT INTO analysis_history
(
    email_text,
    prediction,
    confidence,
    risk_score,
    risk_level,
    threats,
    analysis
)

VALUES (?, ?, ?, ?, ?, ?, ?)
""",
(
    email_text,
    result,
    float(confidence),
    int(risk_score),
    risk_level,
    ", ".join(threats),
    analysis
))

    conn.commit()

    conn.close()

    # =================================
    # Render
    # =================================

    return render_template(
        "index.html",
        prediction=result,
        confidence=round(
            confidence,
            2
        ),
        risk_score=risk_score,
        risk_level=risk_level,
        safe_prob=round(
            safe_probability,
            2
        ),
        phishing_prob=round(
            phishing_probability,
            2
        ),
        threats=threats,
        urls_found=urls_found,
        result_class=result_class,
        analysis=analysis
    )

# =====================================
# Run App
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )