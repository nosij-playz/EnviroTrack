from datatake import WeatherFeatureExtractor
from predictor import DisasterPredictor

if __name__ == "__main__":
    # API keys
    locationiq_key = "pk.43818d0e6f5f19cbcf89ee20346ec08e"
    weatherapi_key = "f2af5ed9ad534094ac6124220252905"

    # Model paths
    model_path = "disaster_prediction_model.h5"
    scaler_path = "scaler.pkl"
    label_encoder_path = "label_encoder.pkl"

    # Create extractor and predictor objects
    extractor = WeatherFeatureExtractor(locationiq_key, weatherapi_key)
    predictor = DisasterPredictor(model_path, scaler_path, label_encoder_path)

    # Get location from user
    location_input = input("Enter location (e.g., 'Shoranur, Kerala, India'): ")

    try:
        # Step 1: Extract features from location
        name, lat, lon, features = extractor.extract_features_from_location(location_input)

        print(f"\n✅ Weather features for {name} (Lat: {lat:.4f}, Lon: {lon:.4f}):")
        for key, value in features.items():
            print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")

        # Step 2: Predict disaster
        predicted_label, prediction_probs = predictor.predict_disaster(features)

        print(f"\n📊 Input Features: {features}")
        print(f"🔮 Predicted Disaster: {predicted_label}")

    except ValueError as ve:
        print("❌", ve)
    except Exception as e:
        print("❌ Failed to retrieve data or make prediction:", e)
