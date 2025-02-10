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

Method : POST
Endpoint : `http://<server ip address:port>/register`
Body : `form-data`

- username
- password
- confirmation
- email
- nama

Responses :

1.  Kode 200 : `"Registration success"`
2.  Kode 400 (username kosong) : `"Input username"`
3.  Kode 400 (password kosong) : `"Input password"`
4.  Kode 400 (email kosong) : `"Input email"`
5.  Kode 400 (name kosong) : `"Input name"`
6.  Kode 400 (password dan confirmation tidak sama) : `"Password does not match"`

Contoh :
![Usage Example (Register)](https://github.com/listyantidewi1/flask-rest-api-todo-app/blob/main/static/images/register.png)
