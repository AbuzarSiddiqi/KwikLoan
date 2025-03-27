from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
from model.model import preprocess_input
import random

app = Flask(__name__)

# Load the trained model
model_path = os.path.join('model', 'loan_model.pkl')
try:
    model = pickle.load(open(model_path, 'rb'))
except FileNotFoundError:
    # If model doesn't exist yet, it will be created when model.py runs
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        data = request.form
        
        # Get user input
        name = data.get('name')
        age = int(data.get('age'))
        income = float(data.get('income'))
        employment_status = data.get('employment_status')
        credit_score = int(data.get('credit_score'))
        loan_amount = float(data.get('loan_amount'))
        loan_purpose = data.get('loan_purpose')
        
        # Process input for model prediction
        input_data = preprocess_input(age, income, employment_status, 
                                     credit_score, loan_amount, loan_purpose)
        
        # Make prediction
        if model is not None:
            prediction = model.predict([input_data])[0]
            probability = int(model.predict_proba([input_data])[0][1] * 100)
        else:
            # If model is not available, use a simplified calculation
            # Higher credit score, income and stable employment increase probability
            credit_factor = (credit_score - 300) / 600  # Normalize 300-900 to 0-1
            income_loan_ratio = min(income / (loan_amount * 2), 1)
            emp_stability = {
                'Government': 0.9,
                'Public-Sector': 0.8,
                'Private': 0.7,
                'Self-employed': 0.6,
                'Retired': 0.5,
                'Unemployed': 0.2
            }.get(employment_status, 0.5)
            
            probability_raw = (credit_factor * 0.4 + income_loan_ratio * 0.3 + emp_stability * 0.2)
            probability_raw = min(max(probability_raw + random.uniform(-0.1, 0.1), 0), 1)
            probability = int(round(probability_raw * 100))
            prediction = probability >= 60  # Approval threshold
            
        # Generate bank logos (SVG icons for different banks)
        bank_logos = {
            "SBI": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
            "HDFC": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><rect width="20" height="16" x="2" y="4" fill="none" stroke="currentColor" stroke-width="2" rx="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M2 10h20M6 14h2M12 14h4"/></svg>',
            "ICICI": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 22V12M2 8.5l10 3.5l10-3.5"/></svg>',
            "Axis": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 2v20M2 12h20"/></svg>',
            "Kotak": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><path fill="none" stroke="currentColor" stroke-width="2" d="M8 2h8l4 4v12l-4 4H8l-4-4V6z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 2v20"/></svg>',
            "BOB": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 3L2 12h4v9h12v-9h4L12 3z"/></svg>',
            "PNB": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><rect x="2" y="4" width="20" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 10h8" stroke="currentColor" stroke-width="2"/><path d="M12 7v10" stroke="currentColor" stroke-width="2"/></svg>',
            "Canara": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40" height="40"><path d="M3 5a2 2 0 012-2h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v10M7 12h10" stroke="currentColor" stroke-width="2"/></svg>'
        }
        
        # Mock data for Indian banks and interest rates
        banks = [
            {"name": "State Bank of India", "logo": bank_logos["SBI"], "interest": round(6.5 + random.uniform(0, 1.5), 1), "processing_fee": "0.35", "tenure": "Up to 30 years", "eligibility": probability > 60, "website_url": "https://www.onlinesbi.sbi/"},
            {"name": "HDFC Bank", "logo": bank_logos["HDFC"], "interest": round(6.8 + random.uniform(0, 1.2), 1), "processing_fee": "0.50", "tenure": "Up to 25 years", "eligibility": probability > 65, "website_url": "https://www.hdfcbank.com/personal/borrow/popular-loans"},
            {"name": "ICICI Bank", "logo": bank_logos["ICICI"], "interest": round(7.2 + random.uniform(0, 1.3), 1), "processing_fee": "0.40", "tenure": "Up to 20 years", "eligibility": probability > 60, "website_url": "https://www.icicibank.com/personal-banking/loans"},
            {"name": "Axis Bank", "logo": bank_logos["Axis"], "interest": round(7.0 + random.uniform(0, 1.4), 1), "processing_fee": "0.45", "tenure": "Up to 30 years", "eligibility": probability > 68, "website_url": "https://www.axisbank.com/retail/loans"},
            {"name": "Kotak Mahindra Bank", "logo": bank_logos["Kotak"], "interest": round(7.5 + random.uniform(0, 1.2), 1), "processing_fee": "0.50", "tenure": "Up to 20 years", "eligibility": probability > 63, "website_url": "https://www.kotak.com/en/personal-banking/loans.html"},
            {"name": "Bank of Baroda", "logo": bank_logos["BOB"], "interest": round(6.9 + random.uniform(0, 1.3), 1), "processing_fee": "0.30", "tenure": "Up to 25 years", "eligibility": probability > 55, "website_url": "https://www.bankofbaroda.in/personal-banking/loans"},
            {"name": "Punjab National Bank", "logo": bank_logos["PNB"], "interest": round(7.1 + random.uniform(0, 1.1), 1), "processing_fee": "0.25", "tenure": "Up to 20 years", "eligibility": probability > 50, "website_url": "https://www.pnbindia.in/personal-banking-loans.html"},
            {"name": "Canara Bank", "logo": bank_logos["Canara"], "interest": round(7.3 + random.uniform(0, 1.0), 1), "processing_fee": "0.35", "tenure": "Up to 20 years", "eligibility": probability > 55, "website_url": "https://www.canarabank.com/retail-loans.aspx"}
        ]
        
        # Filter eligible banks
        eligible_banks = [bank for bank in banks if bank["eligibility"]]
        
        # Return prediction result
        return render_template('result.html', 
                              name=name,
                              prediction=prediction, 
                              probability=probability,
                              banks=eligible_banks)
    
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
