import os
from pathlib import Path

class Config:
    # Base directory of the application
    BASE_DIR = Path(__file__).resolve().parent

    # Data directory
    DATA_DIR = BASE_DIR / 'data'
    os.makedirs(DATA_DIR, exist_ok=True)  # Créer le dossier data s'il n'existe pas

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(str(DATA_DIR), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = BASE_DIR / 'app' / 'static' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Model path
    MODEL_PATH = BASE_DIR / 'app' / 'models' / 'malaria_detector_full.h5'

    @classmethod
    def init_app(cls, app):
        # Créer les dossiers nécessaires
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True) 