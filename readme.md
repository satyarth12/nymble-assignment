## Retail Store Management System

### Tech Stacks Used

- Python as the primary language.
- Django REST Framework for designing and executing APIs.
- PostgreSQL as a better database system

### Project Setup

- **Installing dependencies**

  - `pip install poetry`
  - `poetry install` : This will install all the required dependencies from .toml file.

- **Running the Django server**

  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - `python manage.py runserver`

- **Swagger Documentation**
  - For proper understaning of API's usage: `http://127.0.0.1:8000/`
  - \***\*NOTE: To use the APIs, backend requires user to be authenticated. So, create an auth token from admin pannel for the access.\*\***
