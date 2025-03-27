import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import os

# This function will be used in app.py to preprocess user input
def preprocess_input(age, income, employment_status, credit_score, loan_amount, loan_purpose):
    # Employment status encoding
    emp_status_map = {
        'government': 5,
        'private': 4,
        'public-sector': 4,
        'self-employed': 3,
        'unemployed': 1,
        'retired': 2,
        'other': 0
    }
    
    # Loan purpose encoding
    purpose_map = {
        'home': 5,
        'education': 4,
        'vehicle': 4,
        'business': 3,
        'personal': 2,
        'agriculture': 3,
        'gold': 4,
        'other': 1
    }
    
    # Convert to numerical values
    employment_status_code = emp_status_map.get(employment_status.lower(), 0)
    loan_purpose_code = purpose_map.get(loan_purpose.lower(), 1)
    
    # Normalize income and loan amount (Indian context)
    # Convert to lakhs for normalization
    income_lakhs = income / 100000
    loan_amount_lakhs = loan_amount / 100000
    
    # Create feature array
    features = [
        age, 
        income_lakhs,  # Normalized to lakhs
        employment_status_code,
        credit_score,
        loan_amount_lakhs,  # Normalized to lakhs
        loan_purpose_code
    ]
    
    return features

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic data for model training"""
    np.random.seed(42)
    
    # Generate random features with Indian context
    ages = np.random.randint(21, 65, n_samples)
    
    # Income in lakhs (₹) - Indian context
    incomes = np.random.normal(6, 4, n_samples) * 100000  # Average 6 lakhs per annum
    
    employment_statuses = np.random.choice([0, 1, 2, 3, 4, 5], n_samples, 
                                         p=[0.05, 0.1, 0.1, 0.15, 0.5, 0.1])
    
    # CIBIL scores range from 300-900 in India
    credit_scores = np.random.randint(300, 900, n_samples)
    
    # Loan amounts in lakhs
    loan_amounts = np.random.normal(15, 10, n_samples) * 100000  # Average 15 lakhs
    
    loan_purposes = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.2, 0.2, 0.3, 0.2])
    
    # Create dataframe
    df = pd.DataFrame({
        'age': ages,
        'income': incomes,
        'employment_status': employment_statuses,
        'credit_score': credit_scores,
        'loan_amount': loan_amounts,
        'loan_purpose': loan_purposes
    })
    
    # Create target variable based on rules adapted for Indian context
    # Higher probability of approval for:
    # - Higher CIBIL scores (weight increased)
    # - Higher income relative to loan amount (important in Indian banking)
    # - Stable government/private employment (critical in India)
    # - Age factors (banks prefer 30-50 age range in India)
    
    approval_probability = (
        ((df['credit_score'] - 300) / 600) * 0.4 +  # 40% weight to CIBIL score
        np.minimum(df['income'] / (df['loan_amount'] * 2), 1) * 0.3 +  # 30% weight to income-to-loan ratio
        (df['employment_status'] / 5) * 0.2 +  # 20% weight to employment
        (1 - np.abs((df['age'] - 40) / 40)) * 0.1  # 10% weight to age (preference for 30-50 age range)
    )
    
    # Add some randomness
    approval_probability = np.clip(approval_probability + np.random.normal(0, 0.1, n_samples), 0, 1)
    
    # Generate binary target (approved/rejected)
    df['approved'] = (approval_probability >= 0.6).astype(int)
    
    return df

def train_model():
    """Train and save the loan prediction model"""
    # Generate synthetic data
    df = generate_synthetic_data(5000)
    
    # Features and target
    X = df.drop('approved', axis=1)
    y = df['approved']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save model
    os.makedirs(os.path.dirname('model/loan_model.pkl'), exist_ok=True)
    with open('model/loan_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved to model/loan_model.pkl")
    
    return model

if __name__ == "__main__":
    train_model()
