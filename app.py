from flask import Flask, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import MySQLdb
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# MySQL configuration
db_config = {
    "host": "listyantidewi.mysql.pythonanywhere-services.com",
    "user": "listyantidewi",
    "password": "SMKbisa1234",
    "database": "listyantidewi$todo"
}

def get_db_connection():
    return MySQLdb.connect(**db_config)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return "Please login first", 403
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["POST"])
def register():
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    name = request.form.get("name")
    confirmation = request.form.get("confirmation")

    if not username or not password or not email or not name:
        return "Missing required fields", 400
    if password != confirmation:
        return "Passwords do not match", 400

    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    if cursor.fetchone():
        return "Username or email already taken", 400

    hash_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, name, password, email) VALUES (%s, %s, %s, %s)", (username, name, hash_pw, email))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    session["user_id"] = user["id"]
    session["name"] = user["name"]
    conn.close()
    return "Registration success", 200

@app.route("/login", methods=["POST"])
def login():
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password", 403

    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password"], password):
        return "Invalid username or password", 403

    session["user_id"] = user["id"]
    session["name"] = user["name"]
    return jsonify("login sucessful", session["user_id"], session["name"]), 200

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out successfully", 200


# Categories CRUD

# add category
@app.route("/categories", methods=["POST"])
@login_required
def add_category():
    category = request.form.get("category")

    if not category:
        return "Category name is required", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (user_id, category) VALUES (%s, %s)", (session["user_id"], category))
    conn.commit()
    conn.close()

    return "Category added successfully", 200


# view all categories
@app.route("/categories", methods=["GET"])
@login_required
def view_categories():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, category FROM categories WHERE user_id = %s", (session["user_id"],))
    categories = cursor.fetchall()
    conn.close()
    if not categories:
        return "No categories found", 404
    return jsonify(categories), 200


# edit a category
@app.route("/categories", methods=["PUT"])
@login_required
def edit_category():
    category_id = request.form.get("category_id")
    new_name = request.form.get("new_name")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET category = %s WHERE id = %s AND user_id = %s", (new_name, category_id, session["user_id"]))
    conn.commit()
    conn.close()
    return "Category updated successfully", 200


# delete a category
@app.route("/categories", methods=["DELETE"])
@login_required
def delete_category():
    category_id = request.form.get("category_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s AND user_id = %s", (category_id, session["user_id"]))
    conn.commit()
    conn.close()
    return "Category deleted successfully", 200


# Tasks CRUD

# add new task
@app.route("/tasks", methods=["POST"])
@login_required
def add_task():
    category_id = request.form.get("category_id")
    task = request.form.get("task")

    if not category_id or not task:
        return "Category ID and task description are required", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, category_id, task, status) VALUES (%s, %s, %s, 'pending')",
                   (session["user_id"], category_id, task))
    conn.commit()
    conn.close()

    return "Task added successfully", 200

# view all tasks
@app.route("/tasks", methods=["GET"])
@login_required
def view_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT tasks.id, category_id, categories.category, task, status FROM tasks JOIN categories ON tasks.category_id = categories.id WHERE tasks.user_id = %s", (session["user_id"],))
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        return "No tasks found", 404
    return jsonify(tasks), 200

# edit a task
@app.route("/tasks", methods=["PUT"])
@login_required
def edit_task():
    task_id = request.form.get("task_id")
    new_task = request.form.get("new_task")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task = %s WHERE id = %s AND user_id = %s", (new_task, task_id, session["user_id"]))
    conn.commit()
    conn.close()
    return "Task updated successfully", 200


# delete a task
@app.route("/tasks", methods=["DELETE"])
@login_required
def delete_task():
    task_id = request.form.get("task_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, session["user_id"]))
    conn.commit()
    conn.close()
    return "Task deleted successfully", 200


@app.route("/tasks/complete", methods=["POST"])
@login_required
def complete_task():
    task_id = request.form.get("task_id")

    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    # Check if the task exists
    cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, session["user_id"]))
    task = cursor.fetchone()

    print(f"Task ID: {task_id}, User ID: {session['user_id']}, Task Found: {task}")

    if not task:
        conn.close()
        return "Task not found", 404

    # Update query allows both empty ('') and 'pending' status
    cursor.execute("UPDATE tasks SET status = 'complete' WHERE id = %s AND user_id = %s AND (status = '' OR status = 'not complete')", (task_id, session["user_id"]))
    conn.commit()

    print(f"Rows Affected: {cursor.rowcount}")

    if cursor.rowcount == 0:
        conn.close()
        return "Task update failed", 400

    conn.close()
    return "Task marked as 'complete'", 200



# Undo a completed task
@app.route("/tasks/undo", methods=["POST"])
@login_required
def undo_task():
    task_id = request.form.get("task_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'not complete' WHERE id = %s AND user_id = %s", (task_id, session["user_id"]))
    conn.commit()
    conn.close()
    return "Task marked as 'not complete'", 200


if __name__ == "__main__":
    app.run(debug=True)