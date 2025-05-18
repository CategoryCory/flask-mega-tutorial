from typing import Any
from flask import render_template
from app import app

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
