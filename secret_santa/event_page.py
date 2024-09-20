# pylint: disable=duplicate-code
"""This page serves up the event page endpoints"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    g
)

from secret_santa.auth import login_required
from secret_santa.db import get_db

bp = Blueprint("event_page", __name__, url_prefix="/event")

@bp.route("/")
@login_required
def index():
    """
    This is the view that displays the current event info
    """
    event = get_current_event()

    # check if current user has joined this event and pass info to template
    if event is not None:
        event_attendance = get_user_event_attendance(g.user["user_id"], event["event_id"])
        res = get_db().execute(
        "SELECT event_id, user_id FROM event_attendance"
        )
        event_attendance_list =  res.fetchall()
    else:
        event_attendance = None
        event_attendance_list = []


    return render_template("event_page/index.html", event=event, event_attendance=event_attendance,
                           attendance_list=event_attendance_list)


@bp.route("/<int:event_id>/join", methods=("POST",))
@login_required
def join(event_id):
    """
    Creates an event_attendance event
    """
    current_user_id = g.user["user_id"]
    db = get_db()

    if get_user_event_attendance(current_user_id, event_id) is None:
        db.execute(
            "INSERT INTO event_attendance (user_id, event_id, giftee) VALUES (?, ?, ?)",
            (current_user_id, event_id, None),
        )
        db.commit()
    else:
        print("You have already joined this event!")
        
    return redirect(url_for("event_page.index"))

@bp.route("/<int:event_id>/leave", methods=("POST",))
@login_required
def leave(event_id):
    """
    Deletes the event attendance event for the current user
    """
    current_user_id = g.user["user_id"]
    db = get_db()
    db.execute("DELETE FROM event_attendance WHERE user_id = ? AND event_id = ?", (current_user_id, event_id))
    db.commit()
    return redirect(url_for("event_page.index"))


@bp.route("/<int:event_id>/update", methods=("GET", "POST"))
@login_required
def update(event_id):
    """
    This is the view where the event can be updated
    """
    event = get_event(event_id)

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
                (event_date, draw_date, event_description, cost, event_id),
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
    get_event(event_id)
    db = get_db()
    db.execute("DELETE FROM event WHERE event_id = ?", (event_id,))
    db.commit()
    return redirect(url_for("event"))


def get_user_event_attendance(user_id, event_id):
    """
    Returns the event attendance event for the given user and event
    """
    res = get_db().execute(
        "SELECT event_id, user_id FROM event_attendance "
        "WHERE event_id = ? AND user_id = ?",
        (event_id,user_id),
    )
    return res.fetchone()


def get_current_event():
    """
    Get the current event info, or return None
    """
    res = get_db().execute(
        "SELECT event_id, event_date, draw_date, event_description, "
        "cost FROM event ORDER BY event_date DESC"
    )
    event = res.fetchone()

    return event


def get_event(event_id):
    """
    Get the event with the given id, or return none
    """

    res = get_db().execute(
        "SELECT event_id, event_date, draw_date, event_description, cost FROM event "
        "WHERE event_id = ?",
        (event_id,),
    )
    event = res.fetchone()

    return event
