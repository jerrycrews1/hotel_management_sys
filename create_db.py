import sqlite3
import random


def create_db_tables():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE hotels (hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, hotel_name TEXT NOT NULL, tax_perc DECIMAL(2, 2))''')
    c.execute(
        '''CREATE TABLE room_types (room_type_id INTEGER PRIMARY KEY, description TEXT)''')
    c.execute('''CREATE TABLE rooms (room_num INTEGER PRIMARY KEY, room_type_id INTEGER, rate DECIMAL(5, 2), availability INTEGER NULL DEFAULT 1,
                 FOREIGN KEY (room_type_id) REFERENCES room_types (room_type_id))''')
    c.execute('''CREATE TABLE reservations (reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, guest_id INTEGER, check_in DATETIME NOT NULL, check_out DATETIME NOT NULL,
                 FOREIGN KEY (guest_id) REFERENCES guests (guest_id))''')
    c.execute(
        '''CREATE TABLE guests (guest_id INTEGER PRIMARY KEY, phone_number INTEGER UNIQUE NOT NULL, name VARCHAR(50))''')
    c.execute('''CREATE TABLE reservation_has_rooms (reservation_id INTEGER, room_id INTEGER,
                 FOREIGN KEY (reservation_id) REFERENCES reservations (reservation_id),
                 FOREIGN KEY (room_id) REFERENCES rooms (room_id))''')
    c.execute('''CREATE TABLE cancellations (cancellation_id INTEGER PRIMARY KEY NOT NULL, reservation_id INTEGER,
                 FOREIGN KEY (reservation_id) REFERENCES reservations (reservation_id))''')
    c.execute('''CREATE TABLE reservations_archive (reservation_id INTEGER PRIMARY KEY, guest_id INTEGER, check_in DATETIME NOT NULL, check_out DATETIME NOT NULL,
                 FOREIGN KEY (guest_id) REFERENCES guests (guest_id))''')


def create_rooms():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('DELETE FROM rooms')
    conn.commit()
    for number in range(101):
        if number < 21:
            room_number = 100 + number
        elif 20 < number < 41:
            room_number = 200 + number - 20
        elif 40 < number < 61:
            room_number = 300 + number - 40
        elif 60 < number < 81:
            room_number = 400 + number - 60
        else:
            room_number = 500 + number - 80
        room_type = random.randint(1, 4)
        # this changes the king to be more expensive (it has a lower id) and the single to be least expensive.
        rate = (300 // room_type) ^ room_type
        print(rate, room_type)
        c.execute(
            'INSERT INTO rooms (room_num, room_type_id, rate, availability) VALUES (?, ?, ?, ?)', (room_number, room_type, rate, 1))
        conn.commit()

def create_room_types():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('''INSERT INTO room_types (description) VALUES ('king')''')
    c.execute('''INSERT INTO room_types (description) VALUES ('queen')''')
    c.execute('''INSERT INTO room_types (description) VALUES ('double')''')
    c.execute('''INSERT INTO room_types (description) VALUES ('single')''')
    conn.commit()
