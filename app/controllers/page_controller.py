from flask import Blueprint, render_template

bp = Blueprint('pages', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/history')
def history():
    return render_template('history.html') 