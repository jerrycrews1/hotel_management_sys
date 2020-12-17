""" Test for the program.
"""

from main import create_guest
from create_db import create_db_tables, create_room_types, create_rooms
import sqlite3
import pytest
import os


@pytest.fixture
def setup_db():
    """ Fixture to setup the database connection. """
    # Delete the db.
    os.remove("test.db")
    conn = sqlite3.connect('test.db')
    create_db_tables('test.db')
    create_room_types('test.db')
    create_rooms('test.db')
    yield conn


@pytest.fixture
def setup_test_guests(setup_db):
    conn = setup_db
    c = conn.cursor()
    sample_guests = [
        ('2293469023', 'Jim Halpert'),
        ('8008675309', 'Pam Beasley'),
        ('1234567890', 'Meredith Palmer'),
        ('7639283003', 'Toby Flenderson'),
    ]
    c.executemany(
        'INSERT INTO guests (phone_number, name) VALUES (?, ?)', sample_guests)
    conn.commit()
    yield c


def test_entering_guest_in_db(setup_test_guests):
    """ Test the creation of exactly 4 guests in the DB. """
    c = setup_test_guests
    c.execute('SELECT * FROM guests')
    guests = c.fetchall()
    assert len(guests) == 4


