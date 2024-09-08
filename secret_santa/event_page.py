"""This page serves up the user page endpoints"""

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from werkzeug.exceptions import abort
from flask_mail import Mail, Message

from secret_santa.auth import login_required
from secret_santa.db import get_db

# no url prefix parameter, so this is the default page
bp = Blueprint("user_page", __name__, url_prefix="/event")


@bp.route("/")
def index():
    """
    This is the view that displays the event info
    """
    event=get_current_event()
    return render_template("user_page/index.html", event=event)


@bp.route("/<int:user_id>/update", methods=("GET", "POST"))
@login_required
def update(user_id):
    """
    This is the view where the user can update their user info
    """
    user = get_user(user_id)

    if request.method == "POST":
        address = request.form["address"]
        dietary_info = request.form["dietary_info"]
        error = None

        # if not title:
        #    error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE user SET address = ?, dietary_info = ? WHERE id = ?",
                (address, dietary_info, user_id),
            )
            db.commit()
            return redirect(url_for("user_page.index"))

    return render_template("user_page/update.html", user=user)


@bp.route("/<int:user_id>/delete", methods=("POST",))
@login_required
def delete(user_id):
    """
    Deletes the user
    """
    get_user(user_id)
    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("auth.logout"))

def get_current_event():
    """
    Get the current event info, or return None
    """
    user = (
        get_db()
        .execute(
            "SELECT u.id, username, email, address, dietary_info"
            " FROM user u"
            " WHERE u.id = ?",
            (user_id,),
        )
        .fetchone()
    )

    return user