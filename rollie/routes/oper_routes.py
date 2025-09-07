from flask import (
    render_template, flash, redirect,
    url_for
)
from flask_login import (
    current_user, login_required
)

from rollie import app, db
from rollie.models import Community, Notice
from rollie.decorators import operator_required


@app.route('/operator/dashboard', methods=['POST', 'GET'])
@login_required
@operator_required
def operator_dashboard():
    return render_template(
        'operator/dashboard.html', title="Operator"
    )

@app.route('/operator/profile', methods=['POST', 'GET'])
@login_required
@operator_required
def operator_profile():
    return render_template(
        'operator/profile.html', title="Operator"
    )

@app.route("/operator/community/<int:community_id>/toggle_flag", methods=["POST"])
@login_required
@operator_required
def toggle_flag(community_id):
    community = Community.query.get_or_404(community_id)
    community.is_flagged = not community.is_flagged

    if community.is_flagged:
        flash(f"{community.name} has been flagged", "info")
        message = f"Your community \"{community.name}\" has been flagged for high unsorted waste."
    else:
        message = f"Your community \"{community.name}\" has been unflagged"
        flash(f"{community.name} has been unflagged", "info")

    notice = Notice(community_id=community.id, message=message)
    db.session.add(notice)
    db.session.flush()

    for member in community.users:
        notice.recipients.append(member)

    db.session.commit()

    return redirect(url_for("operator_dashboard"))
