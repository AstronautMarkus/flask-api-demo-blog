# Flask API Demo Blog

A simple RESTful API for a To-Do application built with Flask, featured on [my blog](https://blog.astronautmarkus.dev/).

---

> Please, Read the article: [Create a Flask API with Python - Blog AstronautMarkus](https://blog.astronautmarkus.dev/blogs/create-a-flask-api-with-python/)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [License](#license)

---

## Features

- JWT Authentication
- CRUD operations for to-do items
- Input validation & error handling
- MySQL database integration (Flask-SQLAlchemy)
- CORS support
- Environment variable management (`python-dotenv`)
- Gunicorn for production deployment
- SMTP server integration for email functionality

---

## Requirements

- Python 3.12+
- MySQL database
- pip (Python package installer)
- virtualenv (recommended)
- SMTP server

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/astronautmarkus/flask-api-demo-blog.git
   cd flask-api-demo-blog
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=mysecretkey

DB_HOST=localhost
DB_PORT=3306
DB_USER=user
DB_PASSWORD=password
DB_NAME=flask_api_db

JWT_SECRET_KEY=myjwtsecretkey

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

---

## Database Setup

Initialize the database:

```bash
python app/scripts/create_db.py --reset
```

---

## Running the Application

- **Development mode**
  ```bash
  python app.py
  ```

- **Production mode (Gunicorn)**
  ```bash
  gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
  ```

---

## API Endpoints

| Method | Endpoint              | Description                                 | Auth Required |
|--------|----------------------|---------------------------------------------|--------------|
| POST   | `/auth/register`     | Register a new user                         | No           |
| POST   | `/auth/login`        | Login and obtain a JWT token                | No           |
| GET    | `/tasks`             | Get all to-do items                         | No           |
| POST   | `/tasks`             | Create a new to-do item                     | Yes          |
| GET    | `/tasks/<id>`        | Get a specific to-do item by ID             | No           |
| PUT    | `/tasks/<id>`        | Update a specific to-do item by ID          | No           |
| DELETE | `/tasks/<id>`        | Delete a specific to-do item by ID          | No           |
| GET    | `/users`             | Get all users (admin only)                  | No           |
| GET    | `/users/<id>`        | Get a specific user by ID (admin only)      | Yes          |
| PUT    | `/users/<id>`        | Update a specific user by ID (admin only)   | No           |
| DELETE | `/users/<id>`        | Delete a specific user by ID (admin only)   | No           |

---

> Note: I know it's inconsistent to put Auth only on some things, instead of protecting everything, but in the Blog it's only put on some to explain how the middleware that protects them works, thank you for your understanding.

## Usage

Access the API using tools like Postman or curl.

- **Base URL:**  
  - Development: `http://localhost:5000`
  - Production: `http://0.0.0.0:8000`

---

## License

MIT License. See [LICENSE](LICENSE) for details.
