from flask import Flask, request, jsonify
import pickle

# Save the model and scaler
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

app = Flask(__name__)

# Load the model and scaler
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array([data['temperature'], data['vibration'], data['pressure'], 
                         data['temperature_diff'], data['vibration_diff'], data['pressure_diff']]).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    probability = model.predict_proba(features)[:, 1]
    return jsonify({'failure_prediction': int(prediction[0]), 'failure_probability': float(probability[0])})

if __name__ == '__main__':
    app.run(debug=True)
