from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key for securely signing the session cookie.
app.secret_key = "your_secret_key"


# Function to get a connection to the SQLite database.
# It also ensures rows are returned as dictionaries for easy access.
def get_db_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    return connection


# Route to handle user registration.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":  # Handles form submission for user registration.
        username = request.form.get("username")  # Get the username from the form.
        password = request.form.get("password")  # Get the password from the form.
        connection = get_db_connection()
        try:
            # Hash the password for security before storing it.
            hashed_password = generate_password_hash(password)
            # Insert the new user into the `users` table.
            connection.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            connection.commit()
            # Inform the user that registration was successful.
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))  # Redirect to the login page.
        except sqlite3.IntegrityError:
            # If the username already exists, show an error message.
            flash("Username already exists. Try a different one.", "danger")
        finally:
            connection.close()  # Ensure the database connection is closed.
    return render_template("register.html")  # Render the registration page.


# Route to handle user login.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  # Handles form submission for login.
        username = request.form.get("username")  # Get the username from the form.
        password = request.form.get("password")  # Get the password from the form.
        connection = get_db_connection()
        # Retrieve the user record by username.
        user = connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.close()
        if user and check_password_hash(user["password"], password):  # Verify password hash.
            # Store user details in the session.
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("home"))  # Redirect to the homepage.
        else:
            # Show an error message if login fails.
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")  # Render the login page.


# Route to handle user logout.
@app.route("/logout")
def logout():
    session.clear()  # Clear the session data.
    flash("You have been logged out.", "info")  # Inform the user they have logged out.
    return redirect(url_for("login"))  # Redirect to the login page.


# Homepage route, displays the user's tasks.
@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:  # Redirect to login if the user is not authenticated.
        return redirect(url_for("login"))

    connection = get_db_connection()
    if request.method == "POST":  # Handles form submission to add a new task.
        task = request.form.get("task")  # Get the task name from the form.
        priority = request.form.get("priority")  # Get the task priority from the form.
        if task and priority:
            # Insert the new task into the `tasks` table for the logged-in user.
            connection.execute("INSERT INTO tasks (name, priority, user_id) VALUES (?, ?, ?)",
                               (task, int(priority), session["user_id"]))
            connection.commit()
    # Fetch all tasks for the logged-in user, sorted by priority.
    tasks = connection.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY priority",
                               (session["user_id"],)).fetchall()
    connection.close()
    return render_template("index.html", tasks=tasks)  # Render the homepage with tasks.


# Route to edit a task.
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    connection = get_db_connection()
    if request.method == "POST":  # Handles form submission for editing a task.
        new_name = request.form.get("name")  # Get the updated task name from the form.
        new_priority = request.form.get("priority")  # Get the updated priority from the form.
        if new_name and new_priority:
            # Update the task details in the database.
            connection.execute(
                "UPDATE tasks SET name = ?, priority = ? WHERE id = ? AND user_id = ?",
                (new_name, int(new_priority), task_id, session["user_id"])
            )
            connection.commit()
        connection.close()
        return redirect(url_for("home"))  # Redirect to the homepage.

    # Fetch the task details to be edited.
    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"])
    ).fetchone()
    connection.close()
    return render_template("edit.html", task=task)  # Render the edit page with task details.


# Route to mark a task as completed or not completed.
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    connection = get_db_connection()
    # Toggle the completed status of the task.
    connection.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"])
    )
    connection.commit()
    connection.close()
    return redirect(url_for("home"))  # Redirect to the homepage.


# Route to delete a task.
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()
    # Delete the task from the database.
    connection.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"])
    )
    connection.commit()
    connection.close()
    return redirect(url_for("home"))  # Redirect to the homepage.


if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode.
