from datetime import datetime
from app import db

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(50), nullable=False)  # 'positive' or 'negative'
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'result': self.result,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat()
        } 