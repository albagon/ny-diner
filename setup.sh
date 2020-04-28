#!/bin/bash
# Environment variables
DATABASE_URL="postgresql://alba@localhost:5432/nydiner"
DATABASE_TEST_URL="postgresql://alba@localhost:5432/nydiner_test"
USER_TYPE="RESTAURATEUR"
TOKEN_DINER=""
TOKEN_RESTAURATEUR=""
TOKEN_NYDINER_ADMIN=""
FLASK_APP="app.py"
FLASK_DEBUG="True"
FLASK_ENV="development"
echo "Hello World"
