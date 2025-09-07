from flask import render_template

from rollie import app


@app.errorhandler(403)
def forbidden(e):
    return render_template(
        'errors/error.html',
         error_code=403, 
         message="Forbidden: You don't have permission to access this resource."
    ), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/error.html', 
        error_code=404, 
        message="Page Not Found: The page you are looking for does not exist."
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        'errors/error.html', 
        error_code=500, 
        message="Internal Server Error: Something went wrong."
    ), 500
