# Run the application

First start the poetry shell:

poetry shell

When running for the first time, install dependencies

poetry install

Then use the following command to run the app (debug arg optional)

flask --app secret_santa run --debug

# Initialising the database

Before initialising the database, check the set up values in the instance/user-config.ini file. You must update
the admin email and password to your own values first.

The following command initialises the database and adds an admin user and an event using the values in the user-cofig.ini file:

flask --app secret_santa init-db

This will also clear any existing tables and add new ones, so will delete any exisisting data.

# Testing

To run the tests, run:

pytest

To run test coverage, run:

coverage run -m pytest

coverage report

coverage html

