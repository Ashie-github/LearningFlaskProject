from flask import Flask, url_for, request, redirect, render_template, session, flash, g
from functools import wraps
import sqlite3
# flask --app app run

app = Flask(__name__)
app.secret_key = "my precious"
app.database = "sample.db"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))
    return wrap


@app.route("/")
@login_required
def home():
    g.db = connect_db()
    curr = g.db.execute("select * from posts")
    posts = [dict(title=row[0], description=row[1]) for row in curr.fetchall()]
    print(posts)
    g.db.close()
    return render_template("index.html", posts=posts)


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.method == "POST":
            if request.form["username"] != "admin" or request.form["password"] != "admin":
                error = "Invalid credentials. Please try again."
            else:
                session["logged_in"] = True
                flash("You were just logged in!")
                return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return redirect(url_for("welcome"))


def connect_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    app.run(debug=True)
