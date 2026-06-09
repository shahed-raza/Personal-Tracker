from flask import Flask, render_template, request, session, flash
from flask_session import Session

from helpers import get_quote

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

# session["_flashes"] = "flashes"

Session(app)

@app.route("/")
def index():
    flash(get_quote())
    notes = ["Make Flask Application", "Write the back-end", "Learn & Apply the styles"]
    return render_template("notes.html", notes=notes)


@app.route("/log", methods=["GET", "POST"])
def log():
    flash(get_quote())
    return render_template("log.html")


@app.route("/todo", methods=["GET", "POST"])
def todo():
    flash(get_quote())
    return render_template("todo.html")
