import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path
from flask import current_app

class DetectorService:
    def __init__(self):
        self.model = None
        self.input_size = (128, 128)  # Changé de 64x64 à 128x128

    def load_model(self):
        if self.model is None:
            try:
                print("Loading model from:", current_app.config['MODEL_PATH'])
                self.model = tf.keras.models.load_model(current_app.config['MODEL_PATH'])
                # Afficher le résumé du modèle pour debug
                self.model.summary()
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                raise
        return self.model

    def preprocess_image(self, image_path):
        try:
            # Charger et prétraiter l'image
            img = cv2.imread(str(image_path))
            if img is None:
                raise ValueError(f"Failed to load image from {image_path}")
            
            # Convertir BGR en RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionner
            img = cv2.resize(img, self.input_size)
            
            # Normaliser
            img = img.astype('float32') / 255.0
            
            # Ajouter la dimension du batch
            img = np.expand_dims(img, axis=0)
            
            print(f"Preprocessed image shape: {img.shape}")  # Debug
            return img
            
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            raise

    def predict(self, image_path):
        try:
            model = self.load_model()
            processed_image = self.preprocess_image(image_path)
            
            # Faire la prédiction
            prediction = model.predict(processed_image)
            print(f"Raw prediction shape: {prediction.shape}")  # Debug
            print(f"Raw prediction values: {prediction}")  # Debug
            
            # S'assurer que la prédiction est un nombre valide
            prediction_value = float(prediction[0][0])
            if np.isnan(prediction_value):
                raise ValueError("Model returned NaN prediction")
            
            result = 'positive' if prediction_value > 0.5 else 'negative'
            confidence = float(prediction_value if prediction_value > 0.5 else 1 - prediction_value)
            
            print(f"Processed prediction - Result: {result}, Confidence: {confidence}")  # Debug
            
            return {
                'result': result,
                'confidence': confidence
            }
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            raise 