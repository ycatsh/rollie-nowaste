from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from rollie.enums import UserRole


def operator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != UserRole.PLANT_OPERATOR:
            flash("Access denied: plant operator only.", "danger")
            return redirect(url_for("user_dashboard"))
        return f(*args, **kwargs)
    return decorated_function
