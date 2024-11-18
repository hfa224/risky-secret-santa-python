"""Encapsulates draw functionality"""

import random
from collections import deque
from secret_santa.db import get_db


def perform_draw():
    """
    Method that performs the secret santa draw and updates the event attendance entry
    with the user's draw santee
    """

    db = get_db()

    # get a list of the event attendance objects for the event
    res = db.execute(
        "SELECT user_id, username FROM user WHERE has_joined_event = ?",
        (True,),
    )
    joined_user_list = res.fetchall()

    # assign user ids to other user ids
    # Given a list of people, assign each one a secret santa partner
    # then update the "giftee" field in the database
    random.shuffle(joined_user_list)
    partners = deque(joined_user_list)
    partners.rotate()

    # update the database
    for partner, joined_user in zip(partners, joined_user_list):
        print(partner["user_id"])
        print(joined_user["user_id"])

        res = db.execute(
            "SELECT user_id, username FROM user WHERE user_id = ?",
            (partner["user_id"],),
        )

        db.execute(
            "UPDATE user SET giftee = ? " + " WHERE user_id = ?",
            (
                res.fetchall()[0]["username"],
                joined_user["user_id"],
            ),
        )
        db.commit()

    # later add in exclusions etc
