## Retail Store Management System

### Tech Stacks Used

- Python as the primary language.
- Django REST Framework for designing and executing APIs.
- PostgreSQL as a better database system

### Project Setup

- **Installing dependencies**

  - `pip install poetry`
  - `poetry install` : This will install all the required dependencies from .toml file.

- **Making database migrations**

  - `python manage.py makemigrations`
  - `python manage.py migrate`

- **Creating fake Data**

  - `python manage.py main_app_data` This will create five subsequent rows (dummy data) in every Table
  - Superuser credentials, after running above command: \***\*username: admin, password: admin@123\*\***
  - config/usernames.txt has all dummy usernames and password for each account is **User@123**

- **Running the Django server**

  - `python manage.py runserver`

### Swagger Documentation

- For proper understaning of API's usage, visit `http://127.0.0.1:8000/`
- \***\*NOTE: To use the APIs, backend requires user to be authenticated. So, create an auth token, on `http://127.0.0.1:8000/api-token-auth/`, from admin pannel for the access\*\***
