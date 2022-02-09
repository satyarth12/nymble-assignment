## Retail Store Management System

### Tech Stacks Used

- Python as the primary language.
- Django REST Framework for designing and executing APIs.
- PostgreSQL as a better database system

### Project Setup

- **Installing dependencies**

  - `pip install poetry`
  - `poetry install` : This will install all the required dependencies from .toml file.

- **Sorting the raw csv file & storing the data in redis server**

  - `python redis_storage.py`
  - _**Note:**_ _On line 8, enter the unsorted raw csv file name._

- **Running the FastApi server**

  - `uvicorn main:app --reload`

- **To get the device information**

  - `http://127.0.0.1:8000/device/{device_id}`
  - For extra filtration: `http://127.0.0.1:8000/device/{device_id}q={time_stamp}`

- **Redis Commands for redis-cli**

  - `keys *` for getting all the keys in the redis
  - `flushall` for deleting the redis storage

