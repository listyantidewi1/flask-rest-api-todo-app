# import all the required modules and libraries
from cs50 import SQL
import os
from flask import Flask, jsonify, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import login_required


# configure directory for uploaded files
UPLOAD_FOLDER = 'static/uploads'

# configure allowed file extensions to be uploaded
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.sqlite")

# handle file upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# authentication

@app.route("/register", methods=["POST", "GET"])
def register():
    session.clear()
    if request.method=="POST":
        if not request.form.get("username"):
            return "Input username", 400
        elif not request.form.get("password"):
            return "Input password", 400
        elif not request.form.get("email"):
            return "Input email", 400
        elif not request.form.get("name"):
            return "Input name", 400   
        rows = db.execute("select * from users where username = ? or email = ?", request.form.get("username"), request.form.get("email"))

        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        password_repeat = request.form.get("confirmation")

        hash = generate_password_hash(password)
        if len(rows) == 1:
            return "Username is taken", 400
        if password == password_repeat:
            db.execute("insert into users (username, name, password, email) values (?, ?, ?, ?)", username, name, hash, email)

            registered_user = db.execute("select * from users where username = ?", username)
            session["user_id"] = registered_user[0]["id"]
            session["name"] = registered_user[0]["name"]
            return "Registration success", 200
        else:
            return "Password does not match", 400
    else:
        return "Please register first", 400
    

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return "Input username", 403
        elif not request.form.get("password"):
            return "Input password", 403
        rows = db.execute("SELECT * from users where username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return "Wrong username or password", 403
        elif len(rows) == 1:
            session["user_id"] = rows[0]["id"]
            session["name"] = rows[0]["name"]
            return "You were sucessfully logged in", 200
           
    else:
        return "Please login first", 403
    
@app.route("/logout")
def logout():
    session["user_id"] = None
    session["name"] = None
    session.clear
    return "You have successfully logged out", 200


# CRUD

# view all categories
@app.route("/categories", methods=["GET"])
@login_required
def view_categories():
    if request.method=="GET":
        cat = db.execute("select id, category from categories where user_id = ?", session["user_id"])
        return jsonify(cat), 200
    else:
        return "Invalid request", 403

# add category
@app.route("/categories/add", methods=["GET", "POST"])
@login_required
def categories():
    if request.method=="GET":
        cat = db.execute("select id, category from categories where user_id = ?", session["user_id"])
        return jsonify(cat), 200
    elif request.method=="POST":
        if not request.form.get("category"):
            return "Input category", 400
        else:
            newcat = request.form.get("category")
            rows = db.execute("select category from categories where category = ? and user_id = ?", newcat, session["user_id"])
            if rows:
                return "Category already exists", 400
            else:
                db.execute("insert into categories (category, user_id) values (?,?)", newcat, session["user_id"])
                return "Category was successfully added"
        
# edit a category
@app.route("/categories/<id>/edit", methods=["GET", "POST"])
@login_required
def categories_edit(id):
    if request.method == "GET":
        cat = db.execute("select * from categories where id = ? and user_id = ?", id, session["user_id"])[0]
        return jsonify(cat)
    elif request.method == "POST":
        category = request.form.get("category")
        rows = db.execute("select category from categories where category = ? and user_id = ?", category, session["user_id"])
        if rows:
            return "Category already exists", 400
        else:
            db.execute("update categories set category = ? where id = ?", category, id)
            return "The category has been successfully edited", 200

# delete a category
@app.route("/categories/<id>/delete", methods=["GET"])
@login_required
def categories_delete(id):
    db.execute("delete from categories where id = ?", id)
    return "The category has been successfully deleted", 200


# view all tasks
@app.route("/tasks", methods=["GET"])
@login_required
def view_tasks():
    if request.method=="GET":
        tasks = db.execute("select tasks.id, category_id, categories.category, task from tasks inner join categories on tasks.category_id = categories.id")
        return jsonify(tasks), 200
    else:
        return "Invalid request", 403

# add task
@app.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_new_task():
    if request.method=="GET":
        tasks = db.execute("select tasks.id, category_id, categories.category, task from tasks inner join categories on tasks.category_id = categories.id")
        return jsonify(tasks), 200
    elif request.method=="POST":
        if not request.form.get("category_id"):
            return "Input category", 400
        elif not request.form.get("task"):
            return "Input task", 400
        else:
            category_id = request.form.get("category_id")
            task = request.form.get("task")
            db.execute("insert into tasks (category_id, task) values (?, ?)", category_id, task)
            return "Task was successfully added", 200
        
# edit a task
@app.route("/tasks/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(id):
    if request.method == "GET":
        task = db.execute("select * from tasks where id = ?", id)[0]
        return jsonify(task)
    elif request.method == "POST":
        category_id = request.form.get("category_id")
        task = request.form.get("task")
        db.execute("update tasks set category_id = ?, task = ? where id = ?", category_id, task, id)
        return "The task has been successfully edited", 200
    
# delete a task
@app.route("/tasks/<id>/delete", methods=["GET"])
@login_required
def delete_task(id):
    row = db.execute("select * from tasks where id = ?", id)
    if not row:
        return "Task not found", 404
    else:
        db.execute("delete from tasks where id = ?", id)
        return "The task has been successfully deleted", 200