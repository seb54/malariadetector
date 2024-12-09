from flask import request

@app.route('/history')
def history():
    page = request.args.get('page', 1, type=int)
    analyses = Analysis.query.order_by(Analysis.date.desc()).paginate(page=page, per_page=9)
    return render_template('history.html', analyses=analyses) 