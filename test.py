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
    """ Fixture to enter 4 guest into the database. """
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


def test_create_rooms():
    """ Test for the creation of exactly 101 rooms in the DB. """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM rooms')
    num_of_rooms = c.fetchall()
    assert num_of_rooms[0][0] == 100


def test_phone_number():
    """ Test the length of phone number is 10 digits """
    guest1 = '1234567890'
    guest2 = '8567978345'
    guest3 = '4107851467'
    assert len(guest1) == 10
    assert len(guest2) == 10
    assert len(guest3) == 10

    """ raises error if numbers don't equal 10 """
    error1 = '93846283'
    error2 = '91826402859'
    error3 = '2'
    assert len(error1) != '10'
    assert len(error2) != '10'
    assert len(error3) != '10'


def test_test():
    """ Tests that the rate for each room type is correct. """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM rooms GROUP BY room_type_id')
    room_types = c.fetchall()
    assert room_types[0][2] == 301
    assert room_types[1][2] == 148
    assert room_types[2][2] == 103
    assert room_types[3][2] == 79
