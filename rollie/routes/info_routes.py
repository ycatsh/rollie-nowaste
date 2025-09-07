from flask import (
    render_template
)

from rollie import app


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template(
        'info/index.html', 
    )