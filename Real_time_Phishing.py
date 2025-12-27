import joblib
import pandas as pd
import re
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load('phishing_rf_model.joblib')

# Trusted domains
ALLOWLIST = [
    'google.com',
    'classroom.google.com',
    'docs.google.com',
    'microsoft.com',
    'outlook.com',
    'github.com',
    'stackoverflow.com'
]

def extract_features(url):
    features = {}
    parsed = urlparse(url)

    # Basic string features
    features['length'] = len(url)
    features['dots'] = url.count('.')
    features['hyphens'] = url.count('-')
    features['underscores'] = url.count('_')
    features['slashes'] = url.count('/')
    features['at_sign'] = url.count('@')
    features['question_mark'] = url.count('?')
    features['equal_sign'] = url.count('=')
    features['percent'] = url.count('%')
    features['digits'] = sum(c.isdigit() for c in url)
    features['letters'] = sum(c.isalpha() for c in url)

    # Domain-based
    features['domain_length'] = len(parsed.netloc)
    features['subdomains'] = parsed.netloc.count('.') - 1 if parsed.netloc else 0

    # Suspicious patterns (binary flags)
    features['has_ip'] = 1 if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', parsed.netloc) else 0
    features['has_suspicious_tld'] = 1 if parsed.netloc.endswith(('.tk', '.ml', '.ga', '.cf', '.gq')) else 0
    features['has_https'] = 1 if parsed.scheme == 'https' else 0
    features['has_http'] = 1 if parsed.scheme == 'http' else 0
    features['url_contains_login'] = 1 if 'login' in url.lower() else 0
    features['url_contains_secure'] = 1 if 'secure' in url.lower() else 0
    features['url_contains_account'] = 1 if 'account' in url.lower() else 0
    features['url_contains_verify'] = 1 if 'verify' in url.lower() else 0
    features['url_contains_update'] = 1 if 'update' in url.lower() else 0

    # Return as a DataFrame to maintain column names for the model
    return pd.DataFrame([features])


@app.route('/check_url', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        domain_to_check = urlparse(url).netloc if '//' in url else urlparse('http://' + url).netloc
        if any(domain_to_check.endswith(allowed) for allowed in ALLOWLIST):
            return jsonify({
                "is_phishing": False,
                "probability": 0.0,
                "reason": "Allowlisted"
            })
    except Exception:
        pass

    # Extract features using the notebook's logic
    features_df = extract_features(url)

    # Probability: Maps 0 for 'good' and 1 for 'bad'
    prob = model.predict_proba(features_df)[:, 1][0]
    prediction = model.predict(features_df)[0]

    return jsonify({
        "url": url,
        "is_phishing": bool(prediction == 1),
        "probability": float(prob)
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)