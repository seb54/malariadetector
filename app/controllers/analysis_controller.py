import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.services.detector_service import DetectorService
from app.models.analysis import Analysis
from app import db
import traceback

bp = Blueprint('analysis', __name__, url_prefix='/api')
detector_service = DetectorService()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Créer le dossier uploads s'il n'existe pas
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Faire la prédiction
        prediction = detector_service.predict(filepath)
        
        # Sauvegarder l'analyse en base
        analysis = Analysis(
            image_url=f'/static/uploads/{filename}',
            result=prediction['result'],
            confidence=prediction['confidence']
        )
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify({
            'id': analysis.id,
            'result': analysis.result,
            'confidence': analysis.confidence,
            'image_url': analysis.image_url
        })
        
    except Exception as e:
        print(f"Error in analyze: {str(e)}")
        print(traceback.format_exc())  # Affiche la stack trace complète
        return jsonify({'error': str(e)}), 500 