from flask import (
    render_template, url_for, flash, 
    redirect, request
)
from flask_login import (
    login_user, current_user, logout_user
)

from rollie import app, db, bcrypt
from rollie.forms import SignUpForm, SignInForm
from rollie.models import User


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user_profile'))

    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            community_id=form.community.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')

        return redirect(url_for('signin'))

    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('signin.html', title='Sign In', form=form)


@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('index'))
