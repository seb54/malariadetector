from app import create_app
from flask import send_from_directory, render_template, request, jsonify
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import io

app = create_app()

# Charger le modèle avec plus de gestion d'erreurs
try:
    model_path = app.config['MODEL_PATH']
    print(f"Tentative de chargement du modèle depuis : {model_path}")
    
    if not os.path.exists(model_path):
        print(f"ERREUR: Le fichier du modèle n'existe pas à l'emplacement : {model_path}")
        ml_model = None
    else:
        ml_model = tf.keras.models.load_model(str(model_path))
        print("Modèle chargé avec succès!")
except Exception as e:
    print(f"ERREUR lors du chargement du modèle : {str(e)}")
    ml_model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if ml_model is None:
        print("ERREUR: Le modèle n'est pas chargé")
        return jsonify({'error': 'Le modèle n\'est pas disponible. Vérifiez que le fichier existe.'}), 500

    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Aucune image fournie'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
            
        if file and allowed_file(file.filename):
            # Lire l'image directement depuis le flux de données
            img_bytes = file.read()
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((128, 128))  # Redimensionner à 128x128
            img_array = np.array(img) / 255.0  # Normaliser
            
            # Vérifier si l'image est en RGB
            if len(img_array.shape) == 2:  # Image en niveaux de gris
                img_array = np.stack((img_array,) * 3, axis=-1)
            elif img_array.shape[2] == 4:  # Image RGBA
                img_array = img_array[:, :, :3]
            
            # Ajouter la dimension du batch (1, 128, 128, 3)
            img_array = np.expand_dims(img_array, axis=0)
            print(f"Shape de l'image préparée : {img_array.shape}")
            
            # Faire la prédiction avec TensorFlow
            with tf.device('/CPU:0'):  # Forcer l'utilisation du CPU
                predictions = ml_model.predict(img_array, verbose=0)
                prediction_value = float(predictions[0][0])
                is_positive = prediction_value > 0.5
            
            print(f"Prédiction : {prediction_value} ({'positif' if is_positive else 'négatif'})")
            
            return jsonify({
                'result': 'positive' if is_positive else 'negative',
                'confidence': prediction_value
            })
                
    except Exception as e:
        print(f"ERREUR pendant l'analyse : {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('model.html')

if __name__ == '__main__':
    app.run(debug=True) 