Inventory Management Application
--------------------------------

This is an Inventory Management Application built using Python Django and Django REST Framework (DRF). 
It supports product management with basic CRUD (Create, Read, Update, Delete) operations for products.
The application uses JWT (JSON Web Tokens) for authentication, and PostgreSQL as the backend database.


Features
--------
> JWT Authentication: Secure user authentication using JSON Web Tokens.
> Product Management: Create, Read, Update, and Delete products through RESTful API endpoints.
> PostgreSQL Database: Stores all product data in a PostgreSQL database.
> Testing: Comprehensive testing using Django REST framework's APITestCase.
> Logging: Logging is implemented to track activities and events for better debugging and monitoring.
> Postman: Postman is used for API testing.

Requirements
------------
> Python 3.12

> Django 4.x

> Django REST Framework (DRF) 3.x
 
> PostgreSQL

> djangorestframework-simplejwt for JWT authentication


Api Documentation
-----------------
Link : https://documenter.getpostman.com/view/35166923/2sAXxMesbH


Technologies Used
-----------------
Backend: Python, Django, Django REST Framework
Database: PostgreSQL
Authentication: JWT (JSON Web Token)
Testing: APITestCase from Django REST Framework
Logging: Python's built-in logging library



Installation and setup
----------------------
Prerequisites
-------------
Python 3.12
PostgreSQL
Virtual Environment (optional but recommended)



Setup
-----
Clone the repository:
-
```git clone https://github.com/muhammedkm10/Inventory```


Create and activate a virtual environment:
-

```python -m venv env```
```source env/bin/activate ```
#On Windows use ```env\Scripts\activate```

Install dependencies:
-
```pip install -r requirements.txt```

Configure the database:
-

Update the database settings in settings.py to match your PostgreSQL configuration.

Run migrations:
-
```python manage.py migrate```

Create a superuser (for admin access):
-
```python manage.py createsuperuser```

Run the server:
-
```python manage.py runserver```

Use postman or any other tool to test the api and do the  crud operations.


