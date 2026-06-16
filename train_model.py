import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

print("Loading dataset...")

# Load Dataset
df = pd.read_csv("data/phishing_emails.csv")

print("Original Shape:", df.shape)

# Keep only required columns
df = df[['Email Text', 'Email Type']]

# Remove missing values
df = df.dropna()

# Remove empty strings
df = df[df['Email Text'].str.strip() != ""]

# Convert email text to string
df['Email Text'] = df['Email Text'].astype(str)

print("After Cleaning:", df.shape)

# Convert labels
df['Email Type'] = df['Email Type'].map({
    'Safe Email': 0,
    'Phishing Email': 1
})

# Remove rows where mapping failed
df = df.dropna()

print("\nLabel Distribution:")
print(df['Email Type'].value_counts())

# Features and Labels
X = df['Email Text']
y = df['Email Type']

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# TF-IDF Vectorization
print("\nVectorizing text...")

vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Vectorization complete.")

# Train Model
print("\nTraining model...")

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train_vec, y_train)

print("Model training complete.")

# Predictions
y_pred = model.predict(X_test_vec)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print(f"Accuracy: {accuracy:.4f}")
print("=" * 50)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save Model
joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\n" + "=" * 50)
print("Model saved successfully!")
print("Saved Files:")
print("models/phishing_model.pkl")
print("models/vectorizer.pkl")
print("=" * 50)