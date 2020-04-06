# Backend for New York Diner application

## Project Overview

Enhance a previous frontend project and convert it into a full stack application.

### Specification

The original website sources its data from a JSON file but now, a new Postgresql Database
will be integrated, along with other authentication features.

Two models are created in the database:
1. Restaurants
2. Reviews

## Running the server

Remember to “cd” into the application’s folder. To run the development server:

```
$ export HEALTHY=True
$ export DATABASE_URL={the value of SQLALCHEMY_DATABASE_URI}
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=True
$ export FLASK_ENV=development
$ flask run
```

Navigate to Home page [http://localhost:5000](http://localhost:5000)
