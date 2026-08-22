# 📚 OBS — Online Book Store

A full-stack **Online Book Store (OBS)** web application built with **Python and Django**, designed to provide users with a simple and convenient platform for browsing, searching, and purchasing books online.

## 🚀 Features

* 🔐 User registration and login
* 📚 Browse available books
* 🔎 Search books
* 📖 View detailed book information
* 🛒 Add books to cart
* 💳 Checkout and order management
* 👤 User profile management
* 📦 View order details and order history
* 🛠️ Django admin panel for managing books, users, and orders
* 📱 Responsive design for desktop and mobile devices

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Backend

* Python
* Django

### Database

* SQLite

### Tools

* VS Code
* Git & GitHub

## 📂 Project Structure

```text
OBS/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
│
├── OBS/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── mainapp/
    ├── migrations/
    ├── templates/
    ├── static/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/OBS.git
cd OBS
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 🔑 Admin Panel

Django provides an admin dashboard where administrators can manage:

* Books
* Users
* Orders
* Categories
* Other application data

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## 🎯 Project Objective

The main objective of OBS is to demonstrate the development of a practical **e-commerce web application using Django**, including user authentication, product management, shopping cart functionality, order processing, database integration, and responsive UI design.

## 🔮 Future Enhancements

* Online payment gateway integration
* Book reviews and ratings
* Wishlist functionality
* Email notifications
* Advanced book filtering
* Recommendation system
* REST API integration
* Deployment with a production database

## 👨‍💻 Developer

**Akash Chauhan**

* GitHub: https://github.com/akashchauhan1230
* LinkedIn: https://www.linkedin.com/in/akash-chauhan-762319357/

## 📄 License

This project is created for educational and portfolio purposes.
