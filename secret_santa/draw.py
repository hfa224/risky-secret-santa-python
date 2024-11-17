"""Encapsulates draw functionality"""

import random
from collections import deque
from secret_santa.db import get_db


def perform_draw(event_id):
    """
    Method that performs the secret santa draw and updates the event attendance entry
    with the user's draw santee
    """

    db = get_db()

    # get a list of the event attendance objects for the event
    res = db.execute(
        "SELECT event_id, user_id FROM event_attendance WHERE event_id = ?",
        (event_id,),
    )
    event_attendance_list = res.fetchall()
    user_res = db.execute(
        "SELECT user_id, user_name FROM user",
    )
    all_users = user_res.fetchall()

    # assign user ids to other user ids
    # Given a list of people, assign each one a secret santa partner
    # then update the "giftee" field in the database
    random.shuffle(event_attendance_list)
    partners = deque(event_attendance_list)
    partners.rotate()

    # update the database
    for partner, event_attendance in zip(partners, event_attendance_list):
        print(partner["user_id"])
        print(event_attendance["user_id"])

        res = db.execute(
            "SELECT user_id, user_name FROM user WHERE user_id = ?",
            (partner["user_id"],),
        )

        db.execute(
            "UPDATE event_attendance SET giftee = ? " + " WHERE user_id = ?",
            (
                res["user_name"],
                event_attendance["user_id"],
            ),
        )
        db.commit()

    # later add in exclusions etc
