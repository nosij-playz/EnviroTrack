import numpy as np
import joblib
from tensorflow.keras.models import load_model

class DisasterPredictor:
    def __init__(self, model_path, scaler_path, label_encoder_path):
        self.model = load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        self.label_encoder = joblib.load(label_encoder_path)
        self.feature_names = [
            "rainfall_mm",
            "soil_moisture",
            "temperature_c",
            "river_level_m",
            "wind_speed_kmph",
            "humidity_percent",
            "slope_angle_deg",
            "vegetation_index"
        ]

    def predict_disaster(self, input_features: dict):
        # Convert to model input format
        input_array = np.array([[input_features[feat] for feat in self.feature_names]])
        input_scaled = self.scaler.transform(input_array)

        # Predict
        prediction_probs = self.model.predict(input_scaled)
        predicted_class = np.argmax(prediction_probs, axis=1)
        predicted_label = self.label_encoder.inverse_transform(predicted_class)

        return predicted_label[0], prediction_probs[0]

