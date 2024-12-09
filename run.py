from app import create_app, db
from app.models import Analysis
from flask import send_from_directory, render_template, request, jsonify, url_for
import os
from datetime import datetime
import tensorflow as tf
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

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
            # Sécuriser le nom du fichier
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Créer le dossier uploads s'il n'existe pas
            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            print(f"Dossier d'upload : {upload_folder}")
            
            # Sauvegarder l'image
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            print(f"Image sauvegardée : {filepath}")
            
            try:
                # Préparer l'image pour l'analyse
                img = Image.open(filepath)
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
                
                # Sauvegarder l'analyse dans la base de données
                relative_path = filename  # Utiliser juste le nom du fichier
                analysis = Analysis(
                    image_path=relative_path,
                    is_positive=is_positive,
                    date=datetime.utcnow()
                )
                
                db.session.add(analysis)
                db.session.commit()
                print("Analyse sauvegardée en base de données")
                
                return jsonify({
                    'result': 'positive' if is_positive else 'negative',
                    'confidence': prediction_value,
                    'image_url': url_for('serve_uploads', filename=relative_path)
                })
                
            except Exception as e:
                print(f"ERREUR pendant l'analyse : {str(e)}")
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        print(f"ERREUR dans la route analyze : {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def api_history():
    try:
        analyses = Analysis.query.order_by(Analysis.date.desc()).all()
        return jsonify([{
            'id': analysis.id,
            'image_url': url_for('serve_uploads', filename=analysis.image_path),
            'result': 'positive' if analysis.is_positive else 'negative',
            'confidence': 0.95 if analysis.is_positive else 0.05,  # À adapter selon ton modèle
            'created_at': analysis.date.isoformat()
        } for analysis in analyses])
    except Exception as e:
        print(f"ERREUR dans la route api_history : {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Analysis': Analysis
    }

@app.route('/static/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

@app.route('/static/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/history')
def history():
    analyses = Analysis.query.order_by(Analysis.date.desc()).all()
    return render_template('history.html', analyses=analyses)

if __name__ == '__main__':
    with app.app_context():
        print(f"Chemin de la base de données : {app.config['SQLALCHEMY_DATABASE_URI']}")
        try:
            db.create_all()
            print("Base de données créée avec succès!")
        except Exception as e:
            print(f"Erreur lors de la création de la base de données : {str(e)}")
    app.run(debug=True) 