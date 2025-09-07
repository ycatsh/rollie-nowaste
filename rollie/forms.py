from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, 
    SelectField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo,
    Length, ValidationError
)

from rollie.models import User, Community


def get_community_choices():
    """Return a list of tuples (unique_id, name) for SelectField."""
    communities = Community.query.all()
    return [(c.unique_id, f"{c.name} ({c.plant.name})") for c in communities]


class SignUpForm(FlaskForm):
    """User registration form with validation."""

    name = StringField("Enter Name", validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField("Enter Email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter Password", validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    
    community = SelectField(
        "Select Community",
        choices=[],
        validators=[DataRequired()]
    )
    submit = SubmitField("Sign up")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.community.choices = get_community_choices()

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Error: that email is already in use. Please try again.")


class SignInForm(FlaskForm):
    email = StringField('Enter Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')
