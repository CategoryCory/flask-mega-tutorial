from typing import Any
from urllib.parse import urlsplit
import sqlalchemy as sa
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route("/")
@app.route("/index")
@login_required
def index() -> str:
    posts: list[dict[str, Any]] = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland!",
        },
        {
            "author": {"username": "Mark"},
            "body": "Star Wars is awesome!",
        },
    ]
    return render_template("index.html.j2", title="Home", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html.j2', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html.j2", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
