# New York Diner API

## Introduction

The **New York Diner API** will be deployed, managed and scaled in
[Heroku](https://www.heroku.com/platform), a popular cloud platform. Another
tool used in this project is [Gunicorn](https://gunicorn.org/), a pure-Python
HTTP server for WSGI applications.

## General Specifications (as per Udacity's requirements)

1. Models will include at least…
* Two classes with primary keys at at least two attributes each
* One-to-many relationship between classes

2. Endpoints will include at least…
* Two GET requests
* One POST request
* One PATCH request
* One DELETE request

3. Roles will include at least…
* Two roles with different permissions
* Permissions specified for all endpoints

4. Tests will include at least….
* One test for success behaviour of each endpoint
* One test for error behaviour of each endpoint
* At least two tests of RBAC for each role

### DEPLOYED AT HEROKU
Visit [New York Diner API live](https://nydiner.herokuapp.com/).

### Backend

This application features a complete Flask-SQLAlchemy server with a set of
CRUD endpoints. Auth0 has been integrated for authentication.

A Postgresql Database is used along with flask migration features. For more information about the endpoints visit the [NY Diner API collection in Postman](https://documenter.getpostman.com/view/10562557/SzfDxQmm?version=latest).
Please notice the jwt token should be obtained by logging into the app and then
copying it from the url into the corresponding variable in the collection's environment. For testing purposes, 3 users have been created: the Diner, the Restaurateur and the NYdiner_admin. Each one with a different set of permissions.

Two models are created in the database:
1. Restaurants
2. Reviews

### Auth0 Specifications

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new Regular Web Application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:restaurants`
    - `post:restaurants`
    - `post:reviews`
    - `patch:restaurants`
    - `delete:restaurants`
6. Create new roles for:
    - Diner
        - can `get:restaurants`, `post:reviews`
    - Restaurateur
        - can perform all Diner actions
        - can `post:restaurants`, `patch:restaurants`
    - App_admin
        - can perform all Restaurateur actions
        - can `delete:restaurants`
7. Create the `.env` file in the root of your app and add your Auth0 variables and values to it.
```
# .env
AUTH0_CLIENT_ID=YOUR_AUTH0_CLIENT_ID
AUTH0_DOMAIN=YOUR_AUTH0_DOMAIN
AUTH0_CLIENT_SECRET=YOUR_CLIENT_SECRET
AUTH0_AUDIENCE=YOUR_AUDIENCE
AUTH0_CALLBACK_URL=YOUR_CALLBACK_URL
```

### Before running the development server or unit tests

Remember to “cd” into the application’s folder.

1. Initialize and activate a virtual environment 
```
$ python3 -m venv env
$  source env/bin/activate
```
2. Install the dependencies:
```
$ pip3 install -r requirements.txt
```
3. Set the environment variables:
```
$ export DATABASE_URL=the_url_to_your_local_database
$ export DATABASE_TEST_URL=the_url_to_your_local_testing_database
$ export USER_TYPE=DINER or RESTAURATEUR or NYDINER_ADMIN
$ export TOKEN_DINER=a_new_token_for_diner_user_type
$ export TOKEN_RESTAURATEUR=a_new_token_for_restaurateur_user_type
$ export TOKEN_NYDINER_ADMIN=a_new_token_for_nydiner_admin_user_type
```
Please notice the jwt token should be obtained by logging into the app and then
copying it from the url into the corresponding environment variable.
4. Create all the tables
```
$ flask db upgrade
```

### Development Server
1. Set more environment variables:
```
$ export FLASK_DEBUG=True
$ export FLASK_ENV=development
```
2. Run the development server:
```
$ python app.py
```
3. Navigate to Home page [http://localhost:5000](http://localhost:5000)

### Running Unit Tests

1. Make sure you have set environment variables for: USER_TYPE (IT CAN BE DINER, RESTAURATEUR OR NYDINER_ADMIN), DATABASE_TEST_URL, AUTH0_CLIENT_SECRET, AUTH0_CLIENT_ID and the corresponding TOKEN.

2. Run the tests
```
$ python3 test_app.py -v
```

## Frontend

Simple templates for login and logout have been added to this project.

## Contributing

This repository is the result of a project I am working on to finish a Full-Stack Developer Nanodegree Program. Therefore, all contributions are welcome.

## License

New York Diner API is distributed under the [MIT license](LICENSE).
