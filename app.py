from datetime import time
from flask import Flask, render_template, request, flash, redirect
from flask_session import Session
import sqlite3

from helpers import get_quote

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


dbname = "tracker.db"
cx = sqlite3.connect(dbname)
cursor = cx.cursor()


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
            redirect("/log") # js created error element mentioning error

        if time_taken is None or time_taken == "":
            redirect("/log") # js created error element mentioning error
        try:
            time_taken = int(time_taken)
            if time_taken < 1 or 12 < time_taken:
                redirect("/log") # js created error element mentioning error
        except ValueError:
            redirect("/log") # js created error element mentioning error
        if distractions and distractions == "":
            redirect("/log") # js error mentioning, provide non-empty distractions

        if problems and problems == "":
            redirect("/log") # provide non-empty problems

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
        time_left = request.form.get("time-left")
        title = request.form.get("title")
        eta_time_taken = request.form.get("estimated-time-taken")

        if title is None or title == "":
            redirect("/todo") # js error element
        if eta_time_taken is None or eta_time_taken == "":
            redirect("/todo") # error element
        if time_left is None or time_left == "":
            redirect("/todo") # error element

        try:
            time_left = int(time_left)
        except ValueError:
            redirect("/todo") # error message

        if time_left < 1 or 12 < time_left:
            redirect("/todo") # error message

        try:
            eta_time_taken = int(eta_time_taken)
        except ValueError:
            redirect("/todo") # error message

        if eta_time_taken < 1 or 12 < eta_time_taken:
            redirect("/todo") # error message

        time_left -= eta_time_taken

        cursor.execute("""
                       INSERT INTO "todos"
                       ("title", "estimated_hours", "estimated_minutes")
                       VALUES (?, ?, ?)
                       """,
                       (title, eta_time_taken, 0)
        )
        cx.commit()
        time_left_dict = {"hours": time_left, "minutes": 0}
        return render_template("todo.html", time_left=time_left_dict)


    return render_template("todo.html")
