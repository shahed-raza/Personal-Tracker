import sqlite3
from flask import Flask, render_template, request, flash, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import get_quote, login_required, apology

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


dbname = "tracker.db"
cx = sqlite3.connect(dbname)
cursor = cx.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    flash(get_quote())
    notes = ["Make Flask Application", "Write the back-end", "Learn & Apply the styles"]
    return render_template("notes.html", notes=notes)


@app.route("/log", methods=["GET", "POST"])
def log():
    flash(get_quote()) 
    if request.method == "POST":
        # TODO: also consider optional inputs later
        title = request.form.get("title")
        time_taken = request.form.get("time-taken")
        distractions = request.form.get("distractions")
        problems = request.form.get("problems")

        if title is None or title == "":
            return apology("Title of the task is empty or None")

        if time_taken is None or time_taken == "":
            return apology(f"Time taken to do {title} is empty or None")

        try:
            time_taken = int(time_taken)
            if time_taken < 1 or 12 < time_taken:
                return apology("Time taken field is not in between 1 and 12")
        except ValueError:
            return apology("Time taken field is not an integer")

        if distractions and distractions == "":
            return apology("Distractions fields is empty")

        if problems and problems == "":
            return apology("Problems fields is empty")

        cursor.execute("""
                       INSERT INTO "logs"
                       ("title", "distractions", "problems", "time_taken_hours", "time_taken_minutes")
                       VALUES (?, ?, ?, ?, ?)
                       """,
                       (title, distractions, problems, time_taken, 0)
        )
        cx.commit()

    return render_template("log.html")


@app.route("/todo", methods=["GET", "POST"])
def todo():
    # TODO: lot of logical, structural, design errors need to fix
    flash(get_quote())
    # get inputs:
    #   time-left
    #   title
    #   estimated_time_taken
    # error-checking:
    #   title, time_left, eta_time_taken, none, emtpy checks
    #   eta_time_taken conversion, bound checks
    #   time_left conversions, bound checks
    # time-left calculation and reduction if successful to-do task give
    if request.method == "POST":
        # TODO:
        # time-left should be made via javascript, at the client-machine
        # time-left should be taken as input, and the appropriate time which left
        # should be displayed via dom
        # it also, needs to be reduced for succesive todo taks added by the duration of time each task consumes

        title = request.form.get("title")
        eta_time_taken = request.form.get("estimated-time-taken")

        if title is None or title == "":
            return apology("Todo task's title emtpy or None")

        if eta_time_taken is None or eta_time_taken == "":
            return redirect(f"Estimated time taken for {title} is empty or None")

        try:
            eta_time_taken = int(eta_time_taken)
        except ValueError:
            return apology(f"Estimated time taken for {title} is not an integer")

        if eta_time_taken < 1 or 12 < eta_time_taken:
            return apology(f"Estimated time taken for {title} is not in between 1 and 12")

        cursor.execute("""
                       INSERT INTO "todos"
                       ("title", "estimated_hours", "estimated_minutes")
                       VALUES (?, ?, ?)
                       """,
                       (title, eta_time_taken, 0)
        )
        cx.commit()

    return render_template("todo.html")
