from flask import Blueprint, jsonify
from app.models.analysis import Analysis

bp = Blueprint('history', __name__)

@bp.route('/api/history', methods=['GET'])
def get_history():
    analyses = Analysis.query.order_by(Analysis.created_at.desc()).all()
    return jsonify([analysis.to_dict() for analysis in analyses])

@bp.route('/api/history/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    return jsonify(analysis.to_dict()) 