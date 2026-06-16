🛡️ SentinelAI - AI-Powered Phishing Detection Platform

An intelligent cybersecurity platform that combines Machine Learning, Generative AI, and Threat Intelligence techniques to detect phishing emails, analyze risks, extract suspicious URLs, generate security reports, and provide actionable recommendations.

🚀 Features
🔍 Phishing Detection
Detects phishing emails using a trained Machine Learning model.
TF-IDF Vectorization for email text processing.
Achieves approximately 96% classification accuracy on the phishing dataset.
------------------------------------------------------------------------------
🤖 AI Security Analysis
Powered by Google Gemini AI.
Generates professional cybersecurity assessments.
Provides:
Threat Summary
Attack Type
Risk Assessment
Security Recommendations
------------------------------------------------------------------------------
📊 Risk Assessment
Calculates phishing confidence score.
Generates risk scores from 0-100.
Categorizes threats into:
Low
Medium
High
Critical
------------------------------------------------------------------------------
▶️ Running the Project
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/SentinelAI.git

cd SentinelAI
------------------------------------------------------------------------------
2. Create a Virtual Environment
python -m venv venv
Activate the Environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate
------------------------------------------------------------------------------
3. Install Dependencies
pip install -r requirements.txt
------------------------------------------------------------------------------
4. Configure Gemini API

Create a file named:

.env

Add:

GEMINI_API_KEY=YOUR_API_KEY_HERE

Get your API key from:

Google AI Studio
------------------------------------------------------------------------------
5. Create the Database
python database.py

This creates:

database/phishing.db
------------------------------------------------------------------------------
6. Train the Model (If Required)

If model files are not already present:

python train_model.py

This generates:

models/phishing_model.pkl
models/vectorizer.pkl
------------------------------------------------------------------------------
7. Start the Application
python app.py

You should see:

* Running on http://127.0.0.1:5000
------------------------------------------------------------------------------
8. Open in Browser
Visit:

http://127.0.0.1:5000
------------------------------------------------------------------------------

🛠️ Technology Stack
Backend
Python 3.11
Flask

Machine Learning
Scikit-learn
TF-IDF Vectorizer
Logistic Regression

AI Integration
Google Gemini API

Database
SQLite

Frontend
HTML5
CSS3
JavaScript
Chart.js

Reporting
ReportLab