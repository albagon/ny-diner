# New York Diner

## Introduction

In this project, my goal is to apply all the new skills I've learned at
Udacity's Full-Stack Developer Nanodegree. Some of these skills are:

* Coding in Python 3
* Relational Database Architecture
* Modelling Data Objects with SQLAlchemy
* Internet Protocols and Communication
* Developing a Flask API
* Authentication and Access
* Authentication with Auth0
* Authentication in Flask
* Role-Based Access Control (RBAC)
* Testing Flask Applications
* Deploying Applications


The **New York Diner** application will be deployed, managed and scaled in
[Heroku](https://www.heroku.com/platform), a popular cloud platform. Another
tool used in this project is [Gunicorn](https://gunicorn.org/), a pure-Python
HTTP server for WSGI applications.

## General Specifications (as per Udacity's requirements)

1. Models will include at least…
* Two classes with primary keys at at least two attributes each
* [Optional but encouraged] One-to-many or many-to-many relationships
between classes

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


## About the Stack

I have started this application based on a previous project I finished for my
Front-End Developer Nanodegree at Udacity. The original repository can be found
[here](https://github.com/albagon/restaurant-reviews). This application includes
a service worker that creates a seamless offline experience for the users.

### Backend

This application features a complete Flask-SQLAlchemy server with a set of
endpoints. Auth0 has been integrated for authentication.

The original website sources its data from a JSON file but now, a new Postgresql
Database has been integrated, along with other authentication features.

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
    - `post:restaurants`
    - `post:reviews`
    - `patch:restaurants`
    - `delete:restaurants`
    - `delete:reviews`
6. Create new roles for:
    - Diner
        - can `post:reviews`
    - Restaurateur
        - can perform all Diner actions
        - can `post:restaurants`, `patch:restaurants`
    - App_admin
        - can perform all Restaurateur actions
        - can `delete:restaurants`, `delete:reviews`
7. Create the `.env` file in the root of your app and add your Auth0 variables and values to it.
```
# .env
AUTH0_CLIENT_ID=YOUR_AUTH0_CLIENT_ID
AUTH0_DOMAIN=YOUR_AUTH0_DOMAIN
AUTH0_CLIENT_SECRET=YOUR_CLIENT_SECRET
```

### Running the server

Remember to “cd” into the application’s folder. To run the development server:

1. Initialize and activate a virtual environment 
```
$ python3 -m venv env
$  source env/bin/activate
```
2. Install the dependencies:
```
$ pip3 install -r requirements.txt
```
3. Run the development server:
```
$ export DATABASE_URL={the value of SQLALCHEMY_DATABASE_URI}
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=True
$ export FLASK_ENV=development
$ flask run
```
4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

## Frontend

Templates for login and logout have been added to this project.

### Leaflet.js and Mapbox:

This repository uses [leafletjs](https://leafletjs.com/) with [Mapbox](https://www.mapbox.com/).
Mapbox is free to use, and does not require any payment information.

### Note about ES6

Most of the code in this project has been written to the ES6 JavaScript specification for compatibility with modern web browsers and future proofing JavaScript code. As much as possible, this repository will try to maintain use of ES6 in any additional JavaScript added to it.

## Contributing

This repository is the result of a project I am working on to finish a Full-Stack Developer Nanodegree Program. Therefore, all contributions are welcome.

## License

New York Diner is distributed under the [MIT license](LICENSE).
