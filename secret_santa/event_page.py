# pylint: disable=duplicate-code
"""This page serves up the user page endpoints"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from secret_santa.auth import login_required
from secret_santa.db import get_db

# no url prefix parameter, so this is the default page
bp = Blueprint("event_page", __name__, url_prefix="/event")


@bp.route("/")
def index():
    """
    This is the view that displays the event info
    """
    event = get_current_event()
    return render_template("event_page/index.html", event=event)


@bp.route("/<int:event_id>/update", methods=("GET", "POST"))
@login_required
def update(event_id):
    """
    This is the view where the user can update their user info
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
    Deletes the user
    """
    get_event(event_id)
    db = get_db()
    db.execute("DELETE FROM user WHERE event_id = ?", (event_id,))
    db.commit()
    return redirect(url_for("event"))


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
    Get the current event info, or return None
    """

    res = get_db().execute(
        "SELECT event_id, event_date, draw_date, event_description, cost FROM event "
        "WHERE event_id = ?",
        (event_id,),
    )
    event = res.fetchone()

    return event
