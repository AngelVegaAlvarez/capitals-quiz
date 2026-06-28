import random

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, xp

# Configure application
app = Flask(__name__)

# Register my python function xp so that Jinja can use it in my HTML templates
app.jinja_env.filters["xp"] = xp

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show the points of the user"""

    user_id = session["user_id"]

    # Query player's name and points
    rows = db.execute("SELECT player_name, points FROM players WHERE id = ?", user_id)
    player_name = rows[0]["player_name"]
    points = rows[0]["points"]

    # Render index.html with player_name and points
    return render_template("index.html", player_name=player_name, points=points)


@app.route("/history")
@login_required
def history():
    """Show history of the different game quizzes played by the user"""

    user_id = session["user_id"]

    # Query the date and time, along with the respective pointes earned, of all the game quizzes played by the user
    points_history = db.execute(
        "SELECT points_gained, game_date FROM history WHERE player_id = ? ORDER BY game_date DESC",
        user_id,
    )

    # Render history.html with points_history
    return render_template("history.html", points_history=points_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id by clearing any potential session
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query the username
        rows = db.execute(
            "SELECT * FROM players WHERE player_name = ?", request.form.get("username")
        )

        # Ensure username exists and the password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash_password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to the index page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget the user_id
    session.clear()

    # Redirect user to the login form
    return redirect("/")


@app.route("/capitals", methods=["GET", "POST"])
@login_required
def capitals():
    """Ask 10 questions about capitals of countries around the world for the game quiz and evaluate the answer"""

    number_of_questions = 10
    user_id = session["user_id"]

    # User reached route via POST (submitted the quiz form)
    if request.method == "POST":
        # Retrieve the list of questions previously stored in the session
        questions = session.get("questions", [])

        user_answers = []
        # Loop through each question and collect the user's submitted answer
        for i in range(number_of_questions):
            user_answer = request.form.get(f"answer_{i}", "")
            user_answers.append(user_answer)

        player_points = 0
        results = []

        # Compare each user answer with the correct capital
        for i in range(number_of_questions):
            country = questions[i]["country"]
            correct = questions[i]["capital"]
            user = user_answers[i]

            # Check if the user's answer matches the correct capital and update the player's points
            if user.strip().lower() == correct.lower():
                db.execute("UPDATE players SET points = points + 1 WHERE id = ?", user_id)
                player_points += 1

            results.append({ "country": country, "correct": correct, "user": user, "is_correct": user.strip().lower() == correct.lower() })

        # Record this game into the history
        db.execute("INSERT INTO history (player_id, points_gained) VALUES (?, ?)", user_id, player_points)

        # Redirect user to the answers page showing their results
        return render_template("capitals_answer.html", results=results)

    # User reached route via GET (started a new quiz game)
    else:
        # Query all countries and respective capitals, and randomly select 10 for the quiz game
        rows = db.execute("SELECT country, capital FROM capitals")
        chosen = random.sample(rows, number_of_questions)

        # Store the selected questions in the session so POST can access them
        session["questions"] = chosen

        # Redirect user to the page showing the game that asks the selected questions about capitals
        return render_template("capitals.html", questions=chosen)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""

    # User reached route via POST
    if request.method == "POST":
        # Ensure a username was submitted
        username = request.form.get("username")
        if not username:
            return apology("you must provide an username", 400)

        # Ensure a password and its confirmation were submitted
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology("you must provide a password", 400)
        if not confirmation:
            return apology("you must confirm the password", 400)

        # Ensure the password and the confirmation match
        if password != confirmation:
            return apology("the passwords do not match", 400)

        # Hash the password
        hash_pw = generate_password_hash(password)

        # Insert a new user
        try:
            new_user_id = db.execute(
                "INSERT INTO players (player_name, hash_password) VALUES (?, ?)",
                username,
                hash_pw,
            )
        except ValueError:
            return apology("This user already exists", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Redirect to the index page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")