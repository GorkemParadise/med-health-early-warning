from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import json
from pathlib import Path


app = Flask(__name__)
CORS(app) 
MODEL_DIR = Path(__file__).parent.parent
try:
    with open(MODEL_DIR / 'm1.pkl', 'rb') as f:
        m1 = pickle.load(f)  # Random Forest
    with open(MODEL_DIR / 'm2.pkl', 'rb') as f:
        m2 = pickle.load(f)  # Gradient Boosting
    with open(MODEL_DIR / 'm3.pkl', 'rb') as f:
        m3 = pickle.load(f)  # Scaler
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    exit(1)

def calculate_risk(patient_data):
    """Calculate Parkinson's risk from patient data"""
    df = pd.DataFrame([patient_data])
    X_scaled = m3.transform(df)
    
    # Get predictions from both models
    rf_proba = m1.predict_proba(X_scaled)[0]
    gb_proba = m2.predict_proba(X_scaled)[0]
    
    # Ensemble prediction
    ensemble_proba = (rf_proba + gb_proba) / 2
    predicted_severity = int(np.argmax(ensemble_proba))
    
    # Overall risk score
    risk_score = float(ensemble_proba[1] * 33 + ensemble_proba[2] * 66 + ensemble_proba[3] * 100)
    
    return {
        'severity': predicted_severity,
        'risk_score': round(risk_score, 1),
        'probabilities': {
            'none': round(float(ensemble_proba[0]) * 100, 1),
            'mild': round(float(ensemble_proba[1]) * 100, 1),
            'moderate': round(float(ensemble_proba[2]) * 100, 1),
            'severe': round(float(ensemble_proba[3]) * 100, 1)
        },
        'model_predictions': {
            'm1_rf': {
                'none': round(float(rf_proba[0]) * 100, 1),
                'mild': round(float(rf_proba[1]) * 100, 1),
                'moderate': round(float(rf_proba[2]) * 100, 1),
                'severe': round(float(rf_proba[3]) * 100, 1)
            },
            'm2_gb': {
                'none': round(float(gb_proba[0]) * 100, 1),
                'mild': round(float(gb_proba[1]) * 100, 1),
                'moderate': round(float(gb_proba[2]) * 100, 1),
                'severe': round(float(gb_proba[3]) * 100, 1)
            }
        }
    }

def generate_recommendations(severity, risk_score, patient_data):
    """Generate medical recommendations based on assessment"""
    recommendations = {
        'severity_level': ['Minimal Risk', 'Mild Parkinson', 'Moderate Parkinson', 'Advanced Parkinson'][severity],
        'urgency': ['Low', 'Medium', 'High', 'Critical'][severity],
        'doctor_visit': '',
        'treatment': '',
        'follow_up': '',
        'details': [],
        'risk_factors': []
    }
    
    if severity == 0:
        recommendations['doctor_visit'] = 'Annual checkup recommended'
        recommendations['treatment'] = 'Preventive lifestyle modifications'
        recommendations['follow_up'] = 'Yearly follow-up'
        recommendations['details'] = [
            'Regular exercise (3-4 times per week)',
            'Balanced diet (Mediterranean diet recommended)',
            'Mental activities (puzzles, reading, social activities)',
            'Adequate sleep (7-8 hours)',
            'Head trauma prevention'
        ]
    elif severity == 1:
        recommendations['doctor_visit'] = 'Consult neurologist within 1-2 months'
        recommendations['treatment'] = 'Medication therapy recommended'
        recommendations['follow_up'] = 'Every 3-6 months'
        recommendations['details'] = [
            'Levodopa or dopamine agonists should be evaluated',
            'MAO-B inhibitors (Rasagiline, Selegiline) can be considered',
            'Start physical therapy and rehabilitation program',
            'Exercise program (especially balance and strength exercises)',
            'Speech therapy evaluation',
            'Neurological checkup every 3 months'
        ]
    elif severity == 2:
        recommendations['doctor_visit'] = 'URGENT neurologist consultation (1-2 weeks)'
        recommendations['treatment'] = 'Close monitoring + medication therapy required'
        recommendations['follow_up'] = 'Monthly checkup mandatory'
        recommendations['details'] = [
            'Combined medication therapy may be needed (Levodopa + COMT inhibitor)',
            'Medication doses and timing should be optimized',
            'Physical therapy and rehabilitation should be INTENSIFIED',
            'Speech and swallowing therapy',
            'Occupational therapy for daily activities',
            'Motor fluctuations and dyskinesia should be monitored',
            'Monthly neurological checkup REQUIRED',
            'Support group participation recommended'
        ]
    else:
        recommendations['doctor_visit'] = 'IMMEDIATE referral to movement disorders center'
        recommendations['treatment'] = 'Surgical evaluation + intensive medication'
        recommendations['follow_up'] = 'Weekly/bi-weekly checkup'
        recommendations['details'] = [
            'DBS (Deep Brain Stimulation) surgery should be evaluated',
            'Apomorphine infusion pump can be considered',
            'Duodopa (jejunostomy) evaluation',
            'Maximum medication therapy should be optimized',
            'Intensive physical therapy and rehabilitation MANDATORY',
            'Caregiver training and support',
            'Nutritional support (NGT if needed)',
            'Psychiatry consultation (for depression/anxiety)',
            'Home care services arrangement',
            'Weekly/bi-weekly movement disorders specialist follow-up'
        ]
    
    # Risk factors analysis
    if patient_data['age'] > 70:
        recommendations['risk_factors'].append('Advanced age (70+): Increases Parkinson risk')
    if patient_data['tremor_score'] > 3:
        recommendations['risk_factors'].append('High tremor score: Major symptom')
    if patient_data['rigidity'] > 3:
        recommendations['risk_factors'].append('High rigidity: Significant muscle stiffness')
    if patient_data['bradykinesia'] > 3:
        recommendations['risk_factors'].append('Significant bradykinesia: Movement slowness')
    if patient_data['postural_instability'] > 2.5:
        recommendations['risk_factors'].append('Postural instability: High fall risk')
    if patient_data['motor_updrs'] > 40:
        recommendations['risk_factors'].append('High motor UPDRS: Advanced motor symptoms')
    if patient_data['disease_duration'] > 5:
        recommendations['risk_factors'].append('Long disease duration: Progression risk')
    if patient_data['levodopa_response'] < 50:
        recommendations['risk_factors'].append('Low levodopa response: Treatment difficulty')
    
    if not recommendations['risk_factors']:
        recommendations['risk_factors'].append('No major risk factors detected')
    
    return recommendations

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/api/assess', methods=['POST'])
def assess_patient():
    """Main assessment endpoint"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['age', 'motor_updrs', 'tremor_score', 'rigidity', 
                          'bradykinesia', 'postural_instability', 'disease_duration', 
                          'levodopa_response']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Calculate voice features (estimated from tremor)
        patient_data = {
            'age': float(data['age']),
            'motor_updrs': float(data['motor_updrs']),
            'total_updrs': float(data['motor_updrs']) * 1.3,
            'jitter': 0.003 + (float(data['tremor_score']) / 500),
            'shimmer': 0.02 + (float(data['tremor_score']) / 100),
            'nhr': 0.015 + (float(data['tremor_score']) / 200),
            'hnr': 25 - (float(data['tremor_score']) * 3),
            'tremor_score': float(data['tremor_score']),
            'rigidity': float(data['rigidity']),
            'bradykinesia': float(data['bradykinesia']),
            'postural_instability': float(data['postural_instability']),
            'disease_duration': float(data['disease_duration']),
            'levodopa_response': float(data['levodopa_response'])
        }
        
        # Calculate risk
        risk_result = calculate_risk(patient_data)
        
        # Generate recommendations
        recommendations = generate_recommendations(
            risk_result['severity'],
            risk_result['risk_score'],
            patient_data
        )
        
        # Combine results
        response = {
            'success': True,
            'assessment': risk_result,
            'recommendations': recommendations,
            'patient_data': patient_data
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'models': {
            'm1': {
                'name': 'Random Forest',
                'type': 'Ensemble - Random Forest Classifier',
                'trees': 200,
                'accuracy': '~85%',
                'description': 'Primary classification model using multiple decision trees'
            },
            'm2': {
                'name': 'Gradient Boosting',
                'type': 'Ensemble - Gradient Boosting Classifier',
                'estimators': 150,
                'accuracy': '~82%',
                'description': 'Sequential ensemble model for improved predictions'
            },
            'm3': {
                'name': 'Standard Scaler',
                'type': 'Preprocessing - Normalization',
                'description': 'Standardizes features for consistent model input'
            }
        },
        'features': {
            'most_important': [
                {'name': 'Jitter', 'importance': 19.9},
                {'name': 'Bradykinesia', 'importance': 11.6},
                {'name': 'Tremor Score', 'importance': 11.5},
                {'name': 'Rigidity', 'importance': 11.4},
                {'name': 'Shimmer', 'importance': 10.0}
            ]
        },
        'performance': {
            'accuracy': 85,
            'precision': 0.86,
            'recall': 0.85,
            'f1_score': 0.83
        }
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get dataset statistics"""
    try:
        df = pd.read_csv(MODEL_DIR / 'parkinson_dataset.csv')
        
        stats = {
            'total_patients': len(df),
            'severity_distribution': df['parkinson_severity'].value_counts().to_dict(),
            'age_stats': {
                'mean': float(df['age'].mean()),
                'min': float(df['age'].min()),
                'max': float(df['age'].max())
            },
            'motor_updrs_stats': {
                'mean': float(df['motor_updrs'].mean()),
                'min': float(df['motor_updrs'].min()),
                'max': float(df['motor_updrs'].max())
            },
            'correlations': {
                'tremor_severity': float(df[['tremor_score', 'parkinson_severity']].corr().iloc[0, 1]),
                'rigidity_severity': float(df[['rigidity', 'parkinson_severity']].corr().iloc[0, 1]),
                'bradykinesia_severity': float(df[['bradykinesia', 'parkinson_severity']].corr().iloc[0, 1]),
                'motor_updrs_severity': float(df[['motor_updrs', 'parkinson_severity']].corr().iloc[0, 1])
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 80)
    print("PARKINSON DISEASE ASSESSMENT API")
    print("=" * 80)
    print("\n🚀 Starting Flask server...")
    print("📡 API will be available at: http://localhost:3000")
    print("\nEndpoints:")
    print("  GET  /api/health         - Health check")
    print("  POST /api/assess         - Patient assessment")
    print("  GET  /api/model-info     - Model information")
    print("  GET  /api/statistics     - Dataset statistics")
    print("\n" + "=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=3000)