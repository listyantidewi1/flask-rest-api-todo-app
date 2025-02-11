# Instalasi Software

1. Unduh dan install Python https://www.codepolitan.com/blog/cara-install-python-di-windows-macos-dan-linux-lengkap/

2. Unduh dan install DB Browser for SQLite https://sqlitebrowser.org/dl/

3. Unduh, install, dan buat akun Postman https://www.postman.com/

# Instalasi Libraries & Modules

1. Flask :
   Gunakan perintah berikut ini di terminal untuk menginstall Flask (dokumentasi: https://flask.palletsprojects.com/en/stable/installation/)

   `pip install Flask`

2. CS50 :
   Gunakan perintah berikut ini di terminal untuk menginstall CS50 (dokumentasi: https://cs50.readthedocs.io/libraries/cs50/python/)

   `pip install cs50`

3. flask_session :
   Gunakan perintah berikut ini di terminal untuk menginstall flask_session (dokumentasi: https://flask-session.readthedocs.io/en/latest/installation.html)

   `pip install Flask-Session`

# Unduh dan Jalankan Kode Program

1. Unduh, install, dan konfigurasi Git https://git-scm.com/book/id/v2/Memulai-Pengaturan-Awal-Git
2. Jalankan `git clone https://github.com/listyantidewi1/flask-rest-api-todo-app.git` di terminal
3. Pindah directory ke directory root project dengan menjalankan `cd flask-rest-api-todo-app`
4. Jalankan server dengan perintah `flask run` di terminal
5. Gunakan IP Address komputer dalam jaringan lokal dan port yang digunakan oleh aplikasi
   ![Running Server](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/flask_run.png)

# API Documentation

## Register

### Method     : POST
### Endpoint   : `http://<server ip address:port>/register`
### Body       : `form-data`

- username
- password
- confirmation
- email
- nama

### Responses :

1.  Kode 200 : `"Registration success"`
2.  Kode 400 (username kosong) : `"Input username"`
3.  Kode 400 (password kosong) : `"Input password"`
4.  Kode 400 (email kosong) : `"Input email"`
5.  Kode 400 (name kosong) : `"Input name"`
6.  Kode 400 (password dan confirmation tidak sama) : `"Password does not match"`

### Contoh :

![Usage Example (Register)](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/register.png)


## Login

### Method     : POST
### Endpoint   : `http://<server ip address:port>/login`
### Body       : `form-data`

- username
- password

### Responses :

1.  Kode 200 : `"You were sucessfully logged in"`
2.  Kode 403 (username kosong) : `"Input username"`
3.  Kode 403 (password kosong) : `"Input password"`
4.  Kode 400 (username / password salah) : `"Wrong username or password"`

### Contoh :

![Login](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/login.png)


## Logout

### Method     : GET
### Endpoint   : `http://<server ip address:port>/logout`
### Body       : None

### Responses :

Kode 200 : `"You have successfully logged out"`

### Contoh :

![Logout](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/logout.png)


## View All Categories

### Method     : POST
### Endpoint   : `http://<server ip address:port>/categories`
### Body       : none

### Responses :

Kode 200 : Daftar semua kategori dalam format JSON

### Contoh :

![View all categories](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/view_all_categories.png)


## Add New Category

### Method     : POST
### Endpoint   : `http://<server ip address:port>/categories/add`
### Body       : form-data

- category

### Response   :
1. Kode 200 : `"Category was successfully added"`
2. Kode 400 (category belum diisi) : `"Input category"`
3. Kode 400 (category sudah tersedia) : `"Category already exists"`

### Contoh  :
![Add new category](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/add_new_category.png)

### Method     : GET
### Endpoint   : `http://<server ip address:port>/categories/add`
### Body       : none
### Response   : 
1. Kode 200    : Daftar semua kategori dalam format JSON


## Edit Category

### Method     : GET
### Endpoint   : `http://<server ip address:port>/categories/<id_category>/edit`
### Body       : none

### Response   :
1. Kode 200    : Kategori yang dipilih untuk diubah (JSON) 
2. Kode 404 (kategori yang dipilih tidak ditemukan)    : `"Category not found"`

### Contoh     :
![`GET` edit category](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/edit_category_get.png)

### Method     : POST
### Endpoint   : `http://<server ip address:port>/categories/<id_category>/edit`
### Body       : form-data

- category

### Response   :
1. Kode 200    : `"The category has been successfully edited` 
2. Kode 404 (kategori yang dipilih tidak ditemukan)    : `"Category not found"`
3. Kode 400 (kategori sudah tersedia) : `"Category already exists"`

### Contoh     :
![`POST` Edit category](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/edit_category_post.png)