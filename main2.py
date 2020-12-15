""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys
import datetime
import sqlite3


class Room:
    """ Represents a room.

    Attributes:
        rm_number (str): The room number.
        availability (int): 1 if the room is clean, else 2.
                      Set to 1 by default.
        rate (float): The cost of the room.
    """

    def __init__(self, rm_number):
        """ Initializes a Room object from the rooms table in the db.

        Args:
            room_number (int): The room number.

        Side Effects:
            Sets the room_number, availability, room_type_id, and rate attributes.
        """
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()

        c.execute('SELECT * FROM rooms WHERE room_number = ?', (room_number, ))
        room = c.fetchone()

        self.room_number = room[0]
        self.room_type_id = room[1]
        self.rate = room[2]
        self.availability = room[3]


class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        hotel_id (int): The hotel id.
        hotel_name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
    """

    def __init__(self, hotel_id):
        """ Initializes a Hotel object.

        Args:
            hotel_id (int): The hotel id.

        Side Effects:
            Sets the name and tax_perc attribute attributes.
        """
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        c.execute('SELECT * FROM hotels WHERE hotel_id = ?',
                  (hotel_id, ))
        hotel = c.fetchone()

        self.hotel_id = hotel[0]
        self.name = hotel[1]
        self.tax_perc = hotel[2]

        room_list = [x for x in range(1, 21)]
        roomtype = ['single', 'double', 'queen', 'king']
        self.rooms_dict = {}
        self.occupied_rooms = {}

        for num in room_list:
            if num <= 5:
                self.rooms_dict[num] = roomtype[0]
            elif 6 <= num <= 10:
                self.rooms_dict[num] = roomtype[1]
            elif 11 <= num <= 15:
                self.rooms_dict[num] = roomtype[2]
            elif 14 <= num <= 20:
                self.rooms_dict[num] = roomtype[3]

    def t_cost(self):
        """ This method calculates the total cost per reservation
        Return:
            cost(float): The total cost, including tax
        """

        if self.guest_obj.room_type == 'single':
            # + ((90*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (90*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        elif self.guest_obj.room_type == 'double':
            # + ((100*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (100*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        elif self.guest_obj.room_type == 'queen':
            # + ((110*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (110*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        elif self.guest_obj.room_type == 'king':
            # + ((120*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (120*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        cost = cost + (cost*self.tax_perc)
        print(f"{self.guest_obj.name}'s total cost is ${cost:.2f}")

    def occupied(self):
        """
        Uses room type and number of rooms specified by guests to mark rooms as occupied and remove them from the available rooms to choose from.
        If too many rooms are attempting to be booked the method tells the user that there aren't enough rooms available.

        Return:
            possible_rooms (list): a list of available rooms

        """
        possible_rooms = []
        x = 0
        for key, value in self.rooms_dict.items():
            if self.room_type == value:
                possible_rooms.append(key)
        if len(possible_rooms) < self.num_rooms:
            print("Not enough rooms are available.")
        else:
            while x < self.num_rooms:
                self.occupied_rooms[possible_rooms[x]
                                    ] = self.rooms_dict.pop(possible_rooms[x])
                print("Room "+str(possible_rooms[x])+" is now booked.")
                x = x+1
        return possible_rooms


class Guest:
    """ Represents a Guest from the db. 

    Attributes:
        phone_number (str): The guest's phone number.
        name (str): The guests' name.
    """

    def __init__(self, phone_number):
        """ Gathers basic information about guest, the room type they want and their check in and check out dates.
        Args:
            phone_number (str): The guest's phone number.
        Side Effects:
            Sets the name, phone_number, num_rooms, room_type, check_in, check_out attributes.
        """

        self.conn = sqlite3.connect('hotel.db')
        c = self.conn.cursor()
        c.execute('SELECT * FROM guests WHERE phone_number = ?',
                  (phone_number, ))
        guest = c.fetchone()

        self.guest_id = guest[0]
        self.name = guest[2]
        self.phone_number = guest[1]

    def edit_phone_number(self, new_number):
        self.phone_number = new_number
        c = self.conn.cursor()
        c.execute('UPDATE guests SET phone_number = ? WHERE guest_id = ?',
                  (self.phone_number, self.guest_id))
        self.conn.commit()

    def edit_name(self, new_name):
        self.name = new_name
        c = self.conn.cursor()
        c.execute('UPDATE guests SET new_name = ? WHERE guest_id = ?',
                  (self.name, self.guest_id))
        self.conn.commit()


def create_guest():
    name = input("Enter the guest's name: ").capitalize()
    phone_number = input("Enter the guest's phone_number: ")
    # num_rooms = int(
    #     input("Enter how many rooms the guest needs (no more than 5): "))
    # room_type = input(
    #     "Enter the type of room the guest wants (king, queen, double, single): ").casefold()
    # check_in = input('Enter your check in date (Jun 10 2020): ')
    # check_in = datetime.datetime.strptime(check_in, '%b %d %Y')
    # check_in = check_in.replace(hour=13, minute=00)
    # days_staying = int(input("Enter how many days the guest be staying: "))

    # check_out = (check_in + datetime.timedelta(days=days_staying))
    # check_out = check_out.replace(hour=11, minute=00)

    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    insert_statement = 'INSERT INTO guests(name, phone_number) VALUES(?, ?)'
    c.execute(insert_statement, (name, phone_number))
    conn.commit()


def get_guest():
    phone_number = int(input('Enter guest\'s phone number > '))
    guest = Guest(phone_number)
    return guest


def edit_guest():
    guest = get_guest()
    to_edit = int(
        input("What do you want to edit? \n1. Phone Number, \n2. Name\n>"))
    if to_edit == 1:
        new_number = input("Please enter a new phone number (3323449506) >")
        guest.edit_phone_number(new_number)
    elif to_edit == 2:
        new_name = input("Please enter a new name >")
        guest.edit_name(new_name)


def create_hotel():
    tax_perc = float(input('Enter the hotel tax percentage (0.1 for 10%): '))
    name = input("Enter the name of the hotel: ")
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()

    insert_statement = (
        'INSERT INTO hotels(hotel_name, tax_perc) VALUES(?, ?)')
    c.execute(insert_statement, (name, tax_perc))
    conn.commit()

    c.execute('SELECT * FROM hotels ORDER BY hotel_id DESC LIMIT 1')
    hotel = c.fetchone()
    print(hotel)
    return hotel


def get_hotel():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM hotels')
    hotels = c.fetchall()
    for index, hotel in enumerate(hotels):
        print(f'{index}:{hotel[1]}')
    hotel_id = int(input('Which hotel do you want to manage? >'))
    hotel = Hotel(hotel_id)
    return hotel


def create_db_tables():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE hotels (hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, hotel_name TEXT NOT NULL, tax_perc DECIMAL(2, 2))''')
    c.execute(
        '''CREATE TABLE room_types (room_type_id INTEGER PRIMARY KEY, description TEXT)''')
    c.execute('''CREATE TABLE rooms (room_num INTEGER PRIMARY KEY, room_type_id INTEGER, rate DECIMAL(5, 2), availability INTEGER NULL DEFAULT 1,
                 FOREIGN KEY (room_type_id) REFERENCES room_types (room_type_id))''')
    c.execute('''CREATE TABLE reservations (reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, guest_id INTEGER, room_num INTEGER, check_in DATETIME NOT NULL, check_out DATETIME NOT NULL,
                 FOREIGN KEY (guest_id) REFERENCES guests (guest_id),
                 FOREIGN KEY (room_num) REFERENCES rooms(room_num))''')
    c.execute(
        '''CREATE TABLE guests (guest_id INTEGER PRIMARY KEY, phone_number INTEGER UNIQUE NOT NULL, name VARCHAR(50))''')
    c.execute('''CREATE TABLE reservation_has_rooms (reservation_id INTEGER, room_id INTEGER,
                 FOREIGN KEY (reservation_id) REFERENCES reservations (reservation_id),
                 FOREIGN KEY (room_id) REFERENCES rooms (room_id))''')
    c.execute('''CREATE TABLE cancellations (cancellation_id INTEGER PRIMARY KEY NOT NULL, reservation_id INTEGER,
                 FOREIGN KEY (reservation_id) REFERENCES reservations (reservation_id))''')


def main():
    # create_db_tables()
    print('Welcome to the Hotel Management System.')
    hotel_thing = input(
        'Which are you doing? \n1. Managing an Existing Hotel, or \n2. Creating a New Hotel? \n>')
    if int(hotel_thing) == 1:
        hotel = get_hotel()
    elif int(hotel_thing) == 2:
        hotel = create_hotel()
    else:
        return
    print(f'We are managing the {hotel.name} hotel.')
    while True:
        thing = input(
            'What do you want to do? \n1. Manage Guest \n2. Manage Reservation \n3. OTHER (TBD) \n>')
        if int(thing) == 1:
            guest_thing = input(
                'What do you want to do? \n1. Create Guest, \n2. Retrieve Guest \n3. Edit Guest Information \n>')
            if int(guest_thing) == 1:
                create_guest()
            elif int(guest_thing) == 2:
                get_guest()
            elif int(guest_thing) == 3:
                edit_guest()
            else:
                break
        elif int(thing) == 2:
            reservation_thing = input(
                'What do you want to do? \n 1. New Reservation, 2. Alter An Existing Reservation, Cancel Reservation')
            if int(reservation_thing) == 1:
                create_reservation()
            elif int(reservation_thing) == 2:
                alter_reservation()
            elif int(reservation_thing) == 3:
                cancel_reservation()
        elif int(thing) == 3:
            pass
        else:
            break


if __name__ == "__main__":
    main()
