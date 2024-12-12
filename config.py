import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    
    # Configuration du modèle
    MODEL_PATH = os.path.join('app', 'models', 'malaria_detector_full.h5')
    
    # Configuration des uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}