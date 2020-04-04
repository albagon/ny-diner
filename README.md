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

The `./backend` directory contains a completed Flask server with a complete set of
endpoints. Auth0 has been integrated for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Javascript frontend to consume
the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)

## Contributing

This repository is the result of a project I am working on to finish a Full-Stack Developer Nanodegree Program. Therefore, all contributions are considered.

## License

New York Diner is distributed under the [MIT license](LICENSE).
