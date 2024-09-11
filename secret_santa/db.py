"""
Contains db functionality
"""

import sqlite3
import click
from flask import current_app, g


@click.command("init-db")
def init_db_command():
    """
    Creates the cli 'init-db' command
    Clear the existing data and create new tables
    """

    # Clear the existing data and create new tables.
    init_db()
    click.echo("Initialized the database.")


@click.command("add-event")
@click.option("--event_title", prompt="Enter event title")
@click.option("--draw_date", prompt="Enter draw date yyyy-mm-dd")
@click.option("--event_date", prompt="Enter event date yyyy-mm-dd")
@click.option("--event_description", prompt="Event description")
@click.option("--cost", prompt="Maximum spend")
def add_event_command(event_title, draw_date, event_date, event_description, cost):
    """Command line method to add an event to the database"""
    add_event(event_title, draw_date, event_date, event_description, cost)


def init_app(app):
    """
    Returns the database, will create the database if
    it's not already present in the global flask object

    Keyword arguments:
    app -- the flask app
    """

    # Call the close_db function when cleaning up
    app.teardown_appcontext(close_db)

    # Add the defined cli command to the flask app
    app.cli.add_command(init_db_command)

    app.cli.add_command(add_event_command)


def init_db():
    """
    Initialises the db using the schema file. Will
    clear the existing data and create new tables.
    """
    db = get_db()

    # resource location relative to the package
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def add_event(event_title, draw_date, event_date, event_description, cost):
    """
    Initialises the db using the schema file. Will
    clear the existing data and create new tables.
    """
    db = get_db()

    db.execute(
        "INSERT INTO event (event_title, draw_date, event_date, ",
        "event_description, cost) VALUES (?, ?, ?, ?, ?)",
        (event_title, draw_date, event_date, event_description, cost),
    )
    db.commit()


def get_db():
    """
    Returns the database, will create the database if
    it's not already present in the global flask object
    """

    if "db" not in g:
        # create a connection to the datanase
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    If the connection was created, close it
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
    if e is not None:
        print(e)
