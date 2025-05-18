from typing import Any
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index() -> str:
    user: dict[str, str] = {"username": "Bob"}
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
    return render_template("index.html.j2", title="Home", user=user, posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}.")
        return redirect(url_for("index"))
    return render_template("login.html.j2", title="Sign In", form=form)
