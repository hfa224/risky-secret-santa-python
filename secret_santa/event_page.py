# pylint: disable=duplicate-code
"""This page serves up the event page endpoints"""

from flask import Blueprint, flash, redirect, render_template, request, url_for, g

from secret_santa.auth import login_required
from secret_santa.db import get_db
from secret_santa.draw import perform_draw

bp = Blueprint("event_page", __name__, url_prefix="/event")


@bp.route("/")
@login_required
def index():
    """
    This is the view that displays the current event info
    """
    event = get_current_event()
    return render_template("event_page/index.html", event=event, user=g.user)


@bp.route("/join", methods=("POST",))
@login_required
def join():
    """
    Updates the user to indicate they've joined
    """
    current_user_id = g.user["user_id"]
    db = get_db()

    if not g.user["has_joined_event"]:
        db.execute(
            "UPDATE user SET has_joined_event = ? " + " WHERE user_id = ?",
            (
                True,
                current_user_id,
            ),
        )
        db.commit()
    else:
        print("You have already joined this event!")
    return redirect(url_for("event_page.index"))


@bp.route("/leave", methods=("POST",))
@login_required
def leave():
    """
    Updates user to set has_joined_event to False
    """
    current_user_id = g.user["user_id"]
    db = get_db()

    if g.user["has_joined_event"]:
        db.execute(
            "UPDATE user SET has_joined_event = ? " + " WHERE user_id = ?",
            (
                False,
                current_user_id,
            ),
        )
        db.commit()
    else:
        print("You have already left this event!")
    return redirect(url_for("event_page.index"))


@bp.route("/update", methods=("GET", "POST"))
@login_required
def update():
    """
    This is the view where the event can be updated
    """
    event = get_current_event()

    if request.method == "POST":
        event_date = request.form["event_date"]
        draw_date = request.form["draw_date"]
        event_description = request.form["event_description"]
        cost = request.form["cost"]
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE event SET event_date = ?, draw_date = ?, ",
                "event_description = ?, cost = ?",
                " WHERE event_id = ?",
                (event_date, draw_date, event_description, cost, event["event_id"]),
            )
            db.commit()
            return redirect(url_for("event_page.index"))

    return render_template("event_page/update.html", event=event)


@bp.route("/<int:event_id>/delete", methods=("POST",))
@login_required
def delete(event_id):
    """
    Deletes the event
    """
    db = get_db()
    db.execute("DELETE FROM event WHERE event_id = ?", (event_id,))
    db.commit()
    return redirect(url_for("event"))


@bp.route("/perform_event_draw", methods=("POST",))
@login_required
def perform_event_draw():
    """
    Performs the draw for the event
    """
    perform_draw()
    return redirect(url_for("event_page.index"))


def get_current_event():
    """
    Get the current event info, or return None
    """
    res = get_db().execute(
        "SELECT user_id, event_id, event_date, draw_date, event_description, "
        "cost FROM event ORDER BY event_date DESC"
    )
    event = res.fetchone()

    return event
