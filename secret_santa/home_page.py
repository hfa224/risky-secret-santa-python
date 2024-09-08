"""This page serves up the main page endpoints"""

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

from secret_santa.auth import login_required
from secret_santa.db import get_db
from secret_santa.user_page import get_user

# no url prefix parameter, so this is the default page
bp = Blueprint("index_page", __name__)


@bp.route("/")
def index():
    """
    This is the view that displays the home page
    """
    if g.user:
        user_info = get_user(g.user["user_id"])
    else:
        user_info = None
    return render_template("index.html", user_info=user_info)
