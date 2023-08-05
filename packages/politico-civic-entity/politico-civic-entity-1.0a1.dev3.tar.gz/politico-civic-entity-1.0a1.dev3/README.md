![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-politico-civic-entity

Manage political people and organizations, the POLITICO way.

### Quickstart

1. Install the app.

  ```
  $ pip install politico-civic-entity
  ```

2. Add the app to your Django project settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'entity',
  ]
  ```

3. Migrate the database

  ```
  $ python manage.py migrate entity
  ```


### Developing

##### Running a development server

Move into the example directory, install dependencies and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv install
  $ pipenv run python manage.py runserver
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to `example/.env`.

  ```
  DATABASE_URL="postgres://localhost:5432/entity"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
