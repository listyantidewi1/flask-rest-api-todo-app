# Instalasi Software

1. Unduh dan install Python https://www.codepolitan.com/blog/cara-install-python-di-windows-macos-dan-linux-lengkap/
2. Unduh, install, dan buat akun Postman https://www.postman.com/
3. Unduh, install, dan atur MySQL Server

# Instalasi Libraries & Modules

1. Flask :
   Gunakan perintah berikut ini di terminal untuk menginstall Flask (dokumentasi: https://flask.palletsprojects.com/en/stable/installation/)

   `pip install Flask`

2. flask_session :
   Gunakan perintah berikut ini di terminal untuk menginstall flask_session (dokumentasi: https://flask-session.readthedocs.io/en/latest/installation.html)

   `pip install Flask-Session`

3. Flask MySQL
   Gunakan perintah berikut di terminal untuk menginstall Flask MySQL Database
   `pip install flask-mysqldb`

# Unduh dan Jalankan Kode Program

1. Unduh, install, dan konfigurasi Git https://git-scm.com/book/id/v2/Memulai-Pengaturan-Awal-Git
2. Jalankan `git clone https://github.com/listyantidewi1/flask-rest-api-todo-app.git` di terminal
3. Pindah directory ke directory root project dengan menjalankan `cd flask-rest-api-todo-app`
4. Jalankan server dengan perintah `flask run` di terminal
5. Gunakan IP Address komputer dalam jaringan lokal dan port yang digunakan oleh aplikasi
   ![Running Server](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/flask_run.png)

# Database Schema

```
CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);
```

```
CREATE TABLE `categories` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `category` VARCHAR(255) NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
);
```

```
CREATE TABLE `tasks` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `category_id` INT NOT NULL,
    `task` TEXT NOT NULL,
    `user_id` INT NOT NULL,
    `status` ENUM('complete', 'not complete') NOT NULL DEFAULT 'not complete',
    PRIMARY KEY (`id`),
    FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
);
```

# API Documentation

## Base URL

`https://listyantidewi.pythonanywhere.com/`

## Authentication

All endpoints require a logged-in user session.

### Register

**Endpoint:** `/register`
**Method:** `POST`
**Description:** Register a new user.
**Parameters:**

- `username` (string) - Required
- `password` (string) - Required
- `confirmation` (string) - Must match `password`
- `email` (string) - Required
- `name` (string) - Required
  **Response:**
- `200 OK` - Registration successful
- `400 Bad Request` - Invalid input or username/email taken

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/registerv2.png)

### Login

**Endpoint:** `/login`
**Method:** `POST`
**Description:** Log in an existing user.
**Parameters:**

- `username` (string) - Required
- `password` (string) - Required
  **Response:**
- `200 OK` - Login successful
- `403 Forbidden` - Invalid credentials

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/loginv2.png)

### Logout

**Endpoint:** `/logout`
**Method:** `GET`
**Description:** Log out the current user.
**Response:**

- `200 OK` - Successfully logged out

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/logoutv2.png)

## Categories

### View Categories

**Endpoint:** `/categories`
**Method:** `GET`
**Description:** Retrieve all categories for the logged-in user.
**Response:**

- `200 OK` - Returns a JSON list of categories
- `404 Not Found` - No categories found

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/view_all_categoriesv2.png)

### Add Category

**Endpoint:** `/categories`
**Method:** `POST`
**Description:** Add a new category.
**Parameters:**

- `category` (string) - Required
  **Response:**
- `200 OK` - Category added successfully
- `400 Bad Request` - Missing category name

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/add_new_categoryv2.png)

### Edit Category

**Endpoint:** `/categories`
**Method:** `PUT`
**Description:** Edit an existing category.
**Parameters:**

- `category_id` (integer) - Required
- `new_name` (string) - Required
  **Response:**
- `200 OK` - Category updated successfully

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/edit_categoryv2.png)

### Delete Category

**Endpoint:** `/categories`
**Method:** `DELETE`
**Description:** Delete a category.
**Parameters:**

- `category_id` (integer) - Required
  **Response:**
- `200 OK` - Category deleted successfully

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/delete_categoryv2.png)

## Tasks

### View Tasks

**Endpoint:** `/tasks`
**Method:** `GET`
**Description:** Retrieve all tasks for the logged-in user.
**Response:**

- `200 OK` - Returns a JSON list of tasks
- `404 Not Found` - No tasks found

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/view_all_tasksv2.png)

### Add Task

**Endpoint:** `/tasks`
**Method:** `POST`
**Description:** Add a new task.
**Parameters:**

- `category_id` (integer) - Required
- `task` (string) - Required
  **Response:**
- `200 OK` - Task added successfully
- `400 Bad Request` - Missing required parameters

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/add_new_taskv2.png)

### Edit Task

**Endpoint:** `/tasks`
**Method:** `PUT`
**Description:** Edit an existing task.
**Parameters:**

- `task_id` (integer) - Required
- `new_task` (string) - Required
  **Response:**
- `200 OK` - Task updated successfully

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/edit_taskv2.png)

### Delete Task

**Endpoint:** `/tasks`
**Method:** `DELETE`
**Description:** Delete a task.
**Parameters:**

- `task_id` (integer) - Required
  **Response:**
- `200 OK` - Task deleted successfully

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/delete_taskv2.png)

### Complete Task

**Endpoint:** `/tasks/complete`
**Method:** `POST`
**Description:** Mark a task as complete.
**Parameters:**

- `task_id` (integer) - Required
  **Response:**
- `200 OK` - Task marked as complete

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/complete_a_taskv2.png)

### Undo Completed Task

**Endpoint:** `/tasks/undo`
**Method:** `POST`
**Description:** Undo a completed task.
**Parameters:**

- `task_id` (integer) - Required
  **Response:**
- `200 OK` - Task marked as not complete

![register](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/uncomplete_a_taskv2.png)
