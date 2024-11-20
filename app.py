from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session encryption


def get_db_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        connection = get_db_connection()
        try:
            hashed_password = generate_password_hash(password)
            connection.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            connection.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Try a different one.", "danger")
        finally:
            connection.close()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        connection = get_db_connection()
        user = connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    if request.method == "POST":
        task = request.form.get("task")
        priority = request.form.get("priority")
        if task and priority:
            connection.execute("INSERT INTO tasks (name, priority, user_id) VALUES (?, ?, ?)",
                               (task, int(priority), session["user_id"]))
            connection.commit()
    tasks = connection.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY priority",
                               (session["user_id"],)).fetchall()
    connection.close()
    return render_template("index.html", tasks=tasks)


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    connection = get_db_connection()
    if request.method == "POST":
        new_name = request.form.get("name")
        new_priority = request.form.get("priority")
        if new_name and new_priority:
            connection.execute(
                "UPDATE tasks SET name = ?, priority = ? WHERE id = ? AND user_id = ?",
                (new_name, int(new_priority), task_id, session["user_id"])
            )
            connection.commit()
        connection.close()
        return redirect(url_for("home"))

    # Fetch the task to edit
    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"])
    ).fetchone()
    connection.close()
    return render_template("edit.html", task=task)

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    connection = get_db_connection()
    connection.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"])
    )
    connection.commit()
    connection.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()
    connection.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"])
    )
    connection.commit()
    connection.close()
    return redirect(url_for("home"))

