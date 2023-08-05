![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# politico-civic-election

Create and manage election metadata, the POLITICO way.

### Quickstart

1. Install the app.

  ```
  $ pip install politico-civic-election
  ```

2. Add the app and its dependencies to your Django project.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'entity',
      'geography',
      'government',
      'election',
  ]
```

### Bootstrapping your database

1. Ensure `PROPUBLICA_CONGRESS_API_KEY` is exported into your environment. If you don't have an API key for the ProPublica Congress API, you can request one [here](https://www.propublica.org/datastore/api/propublica-congress-api).

2. Bootstrap the database.

```
$ python manage.py bootstrap_election
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
  DATABASE_URL="postgres://localhost:5432/election"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
