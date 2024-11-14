from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the saved models
reg_dem_pct = joblib.load('models/reg_dem_pct_3_features.pkl')
reg_rep_pct = joblib.load('models/reg_rep_pct_3_features.pkl')
reg_dem_raw = joblib.load('models/reg_dem_raw_3_features.pkl')
reg_rep_raw = joblib.load('models/reg_rep_raw_3_features.pkl')
clf = joblib.load('models/classifier_3_features.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data (these would come from the user input)
    state = request.form['state']
    edu1 = float(request.form['edu1'])
    edu2 = float(request.form['edu2'])
    edu3 = float(request.form['edu3'])

    # Prepare the input features for prediction
    X_test_new = np.array([[edu1, edu2, edu3]])

    # Predict using the classifier (winner)
    winner_pred_new = clf.predict(X_test_new)
    winner = 'Democrat' if winner_pred_new == 1 else 'Republican'

    # Predict using the regressors (percentages and raw votes)
    dem_pct_pred = reg_dem_pct.predict(X_test_new)
    rep_pct_pred = reg_rep_pct.predict(X_test_new)
    dem_raw_pred = reg_dem_raw.predict(X_test_new)
    rep_raw_pred = reg_rep_raw.predict(X_test_new)

    # Prepare the response data
    response = {
        'winner': winner,
        'democrat_votes': f"{dem_pct_pred[0]:.4f}%",
        'republican_votes': f"{rep_pct_pred[0]:.4f}%",
        'democrat_raw': f"{dem_raw_pred[0]:,.0f}",
        'republican_raw': f"{rep_raw_pred[0]:,.0f}",
        'state': state  # Map state index to state name if needed
    }

    return jsonify(response)

# Vercel handles the app automatically, so no need for app.run()
