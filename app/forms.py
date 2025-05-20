import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username: StringField) -> None:
        user = db.session.scalar(
            sa.Select(User).where(User.username == username.data)
        )
        if user is not None:
            raise ValidationError("Please select a different username.")

    def validate_email(self, email: StringField) -> None:
        user = db.session.scalar(
            sa.Select(User).where(User.email == email.data)
        )
        if user is not None:
            raise ValidationError("Please select a different email address.")
