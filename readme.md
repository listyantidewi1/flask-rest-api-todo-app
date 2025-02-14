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


52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
All endpoints require a logged-in user session.
**Endpoint:** `/categories`
**Method:** `POST`
**Description:** Add a new category.
**Parameters:**
- `category` (string) - Required
**Response:**
- `200 OK` - Category added successfully
- `400 Bad Request` - Missing category name

### Edit Category
**Endpoint:** `/categories`
**Method:** `PUT`
**Description:** Edit an existing category.
**Parameters:**
- `category_id` (integer) - Required
- `new_name` (string) - Required
**Response:**
- `200 OK` - Category updated successfully

### Delete Category
**Endpoint:** `/categories`
**Method:** `DELETE`
**Description:** Delete a category.
**Parameters:**
- `category_id` (integer) - Required
**Response:**
- `200 OK` - Category deleted successfully

## Tasks

### View Tasks
**Endpoint:** `/tasks`
**Method:** `GET`
**Description:** Retrieve all tasks for the logged-in user.
**Response:**
- `200 OK` - Returns a JSON list of tasks
- `404 Not Found` - No tasks found

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

### Edit Task
**Endpoint:** `/tasks`
**Method:** `PUT`
**Description:** Edit an existing task.
**Parameters:**
- `task_id` (integer) - Required
- `new_task` (string) - Required
**Response:**
- `200 OK` - Task updated successfully

### Delete Task
**Endpoint:** `/tasks`
**Method:** `DELETE`
**Description:** Delete a task.
**Parameters:**
- `task_id` (integer) - Required
**Response:**
- `200 OK` - Task deleted successfully

### Complete Task
**Endpoint:** `/tasks/complete`
**Method:** `POST`
**Description:** Mark a task as completed.
**Parameters:**
- `task_id` (integer) - Required
**Response:**
- `200 OK` - Task marked as completed

### Undo Completed Task
**Endpoint:** `/tasks/undo`
**Method:** `POST`
**Description:** Undo a completed task.
**Parameters:**
- `task_id` (integer) - Required
**Response:**
- `200 OK` - Task marked as pending
