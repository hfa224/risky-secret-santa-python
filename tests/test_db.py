"""Test db"""

import sqlite3

from dataclasses import dataclass
import pytest
from secret_santa.db import get_db


def test_get_close_db(app):
    """Test get_db"""
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(app, runner, monkeypatch):
    """Test init_db command"""

    @dataclass
    class Recorder:
        """Recorder class"""

        called_init_db = False

    def fake_init_db():
        """fake init db method"""
        Recorder.called_init_db = True

    with app.app_context():
        monkeypatch.setattr("secret_santa.db.init_db", fake_init_db)
        result = runner.invoke(args=["init-db"])
        assert "My Secret Santa Event" in result.output
        assert Recorder.called_init_db
