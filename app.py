"""
app.py
------
Flask backend for the AI-Based Student Admission Prediction System.

Routes:
    GET  /            -> landing page
    GET  /dashboard    -> prediction dashboard
    GET  /history       -> prediction history page
    POST /api/predict   -> runs the trained model and logs the result
    GET  /api/history    -> returns recent predictions as JSON
    GET  /api/stats      -> returns aggregate stats for the dashboard
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

from database import init_db, log_prediction, get_recent_predictions, get_summary_stats

app = Flask(__name__)
init_db()

with open('admission_model.pkl', 'rb') as f:
    saved_data = pickle.load(f)

model = saved_data['model']
category_mapping = saved_data['category_mapping']
feature_importance = saved_data['feature_importance']
model_accuracy = saved_data['accuracy']

FACTOR_LABELS = {
    'avg_academic_score': 'Academic Score (10th/12th average)',
    'entrance_score': 'Entrance Exam Score',
    'category_encoded': 'Category',
    'score_gap_from_cutoff': 'Gap from Previous Cutoff'
}


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        categories=list(category_mapping.keys()),
        accuracy=round(model_accuracy * 100, 2),
        feature_importance=[
            {'label': FACTOR_LABELS.get(f['feature'], f['feature']),
             'value': round(f['importance'] * 100, 1)}
            for f in feature_importance
        ]
    )


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()

    tenth = float(data['tenth_percent'])
    twelfth = float(data['twelfth_percent'])
    entrance = float(data['entrance_score'])
    category = data['category']
    cutoff = float(data['previous_year_cutoff'])

    avg_academic_score = (tenth + twelfth) / 2
    score_gap = entrance - cutoff
    category_encoded = category_mapping.get(category, 0)

    input_features = np.array([[avg_academic_score, entrance, category_encoded, score_gap]])

    probability = model.predict_proba(input_features)[0][1]
    prediction = "High Chance" if probability >= 0.5 else "Low Chance"
    top_factor_key = feature_importance[0]['feature']
    top_factor = FACTOR_LABELS.get(top_factor_key, top_factor_key)

    result = {
        'tenth_percent': tenth,
        'twelfth_percent': twelfth,
        'entrance_score': entrance,
        'category': category,
        'previous_year_cutoff': cutoff,
        'probability': round(probability * 100, 2),
        'prediction': prediction,
        'top_factor': top_factor,
        'score_gap': round(score_gap, 2)
    }

    log_prediction(result)

    return jsonify(result)


@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(get_recent_predictions())


@app.route('/api/stats', methods=['GET'])
def api_stats():
    stats = get_summary_stats()
    stats['model_accuracy'] = round(model_accuracy * 100, 2)
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=False, port=5000)
