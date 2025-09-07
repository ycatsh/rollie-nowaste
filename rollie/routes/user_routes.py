from io import BytesIO

from flask import (
    render_template, send_file, abort
)
from flask_login import (
    current_user, login_required
)
import qrcode

from rollie import app


@app.route('/user/dashboard', methods=['POST', 'GET'])
@login_required
def user_dashboard():
    return render_template(
        'user/dashboard.html', 
    )


@app.route('/user/profile', methods=['POST', 'GET'])
@login_required
def user_profile():
    return render_template('user/profile.html')


@app.route('/user/print_card')
@login_required
def print_card():
    return render_template('user/print_card.html', user=current_user)


@app.route('/user/payments')
@login_required
def payments():
    return render_template('user/payments.html')


@app.route('/user/scans')
@login_required
def user_scans():
    return render_template('user/checkins.html')


@app.route('/user/qr')
@login_required
def serve_qr():
    uid = current_user.unique_id
    if not uid:
        abort(404)

    img = qrcode.make(uid)
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

