# import all the required modules and libraries
from cs50 import SQL
import os
from flask import Flask, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.sqlite")

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
        if not cat:
            return "No categories found", 404
        else:
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
        cat = db.execute("select * from categories where id = ? and user_id = ?", id, session["user_id"])
        if cat:
            return jsonify(cat)
        else:
            return "Category not found", 404
    elif request.method == "POST":
        category = request.form.get("category")
        rows = db.execute("select category from categories where id = ? and category = ? and user_id = ?", id, category, session["user_id"])
        if rows:
            return "Category already exists", 400
        else:
            updateCat = db.execute("update categories set category = ? where id = ? and user_id = ?", category, id, session["user_id"])
            if updateCat:
                return "The category has been successfully edited", 200
            else:
                return "Category not found", 404

# delete a category
@app.route("/categories/<id>/delete", methods=["GET"])
@login_required
def categories_delete(id):
    deleteCat = db.execute("delete from categories where id = ? and user_id = ?", id, session["user_id"])
    if deleteCat:
        return "The category has been successfully deleted", 200
    else:
        return "Category not found", 404

# view all tasks
@app.route("/tasks", methods=["GET"])
@login_required
def view_tasks():
    if request.method=="GET":
        tasks = db.execute("select tasks.id, category_id, categories.category, task, status from tasks inner join categories on tasks.category_id = categories.id where tasks.user_id = ?", session["user_id"])
        if not tasks:
            return "No tasks found", 404
        else:
            return jsonify(tasks), 200
    else:
        return "Invalid request", 403
    

# view completed tasks
@app.route("/tasks/complete", methods=["GET"])
@login_required
def view_complete_tasks():
    if request.method=="GET":
        tasks = db.execute("select tasks.id, category_id, categories.category, task, status from tasks inner join categories on tasks.category_id = categories.id where tasks.user_id = ? and status = 'complete'", session["user_id"])
        if not tasks:
            return "No tasks found", 404
        else:
            return jsonify(tasks), 200
    else:
        return "Invalid request", 403
    
# view not complete tasks
@app.route("/tasks/notcomplete", methods=["GET"])
@login_required
def view_not_complete_tasks():
    if request.method=="GET":
        tasks = db.execute("select tasks.id, category_id, categories.category, task, status from tasks inner join categories on tasks.category_id = categories.id where tasks.user_id = ? and status = 'not complete'", session["user_id"])
        if not tasks:
            return "No tasks found", 404
        else:
            return jsonify(tasks), 200
    else:
        return "Invalid request", 403

# add task
@app.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_new_task():
    if request.method=="GET":
        tasks = db.execute("select tasks.id, category_id, categories.category, task from tasks inner join categories on tasks.category_id = categories.id where tasks.user_id = ?", session["user_id"])
        if not tasks:
            return "No tasks found", 404
        else:
            return jsonify(tasks), 200
    elif request.method=="POST":
        if not request.form.get("category_id"):
            return "Input category", 400
        elif not request.form.get("task"):
            return "Input task", 400
        else:
            category_id = request.form.get("category_id")
            task = request.form.get("task")
            getCatId = db.execute("select id from categories where id = ? and user_id = ?", category_id, session["user_id"])
            if not getCatId:
                return "Category not found", 404
            else:
                getTask = db.execute("select task from tasks where task = ? and user_id = ?", task, session["user_id"])
                if getTask:
                    return "Task already exists", 400
                else:     
                    db.execute("insert into tasks (category_id, task, user_id) values (?, ?, ?)", category_id, task, session["user_id"])
                    return "Task was successfully added", 200
        
# edit a task
@app.route("/tasks/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(id):
    if request.method == "GET":
        task = db.execute("select * from tasks where id = ? and user_id = ?", id, session["user_id"])
        if not task:
            return "Task not found", 404
        else:
            return jsonify(task)
    elif request.method == "POST":
        category_id = request.form.get("category_id")
        task = request.form.get("task")
        getCatId = db.execute("select id from categories where id = ? and user_id = ?", category_id, session["user_id"])
        if not getCatId:
            return "Category not found", 404
        else:
            getTask = db.execute("select task from tasks where task = ? and user_id = ?", task, session["user_id"])
            if getTask:
                return "Task already exists", 400
            else:
                db.execute("update tasks set category_id = ?, task = ? where id = ?", category_id, task, id)
                return "The task has been successfully edited", 200
            
# complete a task
@app.route("/tasks/<id>/complete", methods=["GET"])
@login_required
def complete_task(id):
    if request.method == "GET":
        task = db.execute("select * from tasks where id = ? and user_id = ?", id, session["user_id"])
        if not task:
            return "Task not found", 404
        else:
            check = db.execute("select status from tasks where id = ?", id)
            if check[0]["status"] == "complete":
                return "The task is already completed", 400
            else:
                db.execute("update tasks set status = 'complete' where id = ?", id)
                return "The task has been successfully completed", 200
    else:
        return "Invalid request", 403
    
# undo complete a task
@app.route("/tasks/<id>/uncomplete", methods=["GET"])
@login_required
def uncomplete_task(id):
    if request.method == "GET":
        task = db.execute("select * from tasks where id = ? and user_id = ?", id, session["user_id"])
        if not task:
            return "Task not found", 404
        else:
            check = db.execute("select status from tasks where id = ?", id)
            if check[0]["status"] == "not complete":
                return "The task is already set to 'not complete'", 400
            else:
                db.execute("update tasks set status = 'not complete' where id = ?", id)
                return "The task status has been set to 'not complete'", 200
    else:
        return "Invalid request", 403
    
    
# delete a task
@app.route("/tasks/<id>/delete", methods=["GET"])
@login_required
def delete_task(id):
    row = db.execute("select * from tasks where id = ? and user_id = ?", id, session["user_id"])
    if not row:
        return "Task not found", 404
    else:
        db.execute("delete from tasks where id = ?", id)
        return "The task has been successfully deleted", 200