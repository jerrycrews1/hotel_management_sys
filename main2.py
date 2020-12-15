""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys
import datetime
import sqlite3


class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
        room_type (str): The type of room the guest has requested
        num_rooms (int): The number of rooms the guest has requested
        guest_obj (obj): An object of the Guest class
        rooms_dict (dict): A dictionary where the key is the room number and the value is the room type
        occupied_rooms (dict): A dictionary with rooms that are currently occupied

    """

    def __init__(self, name, tax_perc, guest_obj):
        """ Initializes a Hotel object.

        Args:
            name (str): The name of the hotel.
            tax_perc (float): The tax percentage the hotel is subject to.
            guest_obj (obj): An object of the Guest class

        Side Effects:
            Sets the name, and tax_perc attribute attributes.
        """

        self.name = name
        self.tax_perc = tax_perc
        self.room_type = guest_obj.room_type
        self.num_rooms = guest_obj.num_rooms
        self.guest_obj = guest_obj

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
    """ Represents a Guest. 

    Attributes:
        guest_id (int): The guest_id stored in the db.
    """

    def __init__(self, guest_id):
        """ Gathers basic information about guest, the room type they want and their check in and check out dates.
        Args:
            guest_id (int): The guest_id stored in the db.

        Side Effects:
            Sets the name, phone_number, num_rooms, room_type, check_in, check_out attributes.
        """
        self.guest_id = guest_id
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        guest = c.execute(
            f'''SELECT * FROM guests WHERE guest_id = {guest_id}''').fetchall()[0]

        self.name = guest[1]
        self.phone_number = guest[2]
        self.num_rooms = guest[3]
        self.room_type = guest[4]
        self.days_staying = guest[5]
        self.check_in = guest[6]
        self.check_out = guest[7]


def create_guest():
    name = input("Enter the guest's name: ").capitalize()
    phone_number = input("Enter the guest's phone_number: ")
    num_rooms = int(
        input("Enter how many rooms the guest needs (no more than 5): "))
    room_type = input(
        "Enter the type of room the guest wants (king, queen, double, single): ").casefold()
    check_in = input('Enter your check in date (Jun 10 2020): ')
    check_in = datetime.datetime.strptime(check_in, '%b %d %Y')
    check_in = check_in.replace(hour=13, minute=00)
    days_staying = int(input("Enter how many days the guest be staying: "))

    check_out = (check_in + datetime.timedelta(days=days_staying))
    check_out = check_out.replace(hour=11, minute=00)

    conn = sqlite3.connect('hoteldb')
    c = conn.cursor()
    insert_statement = 'INSERT INTO guests(name, phone_number, num_rooms, room_type, days_staying, check_in, check_out) VALUES(?, ?, ?, ?, ?, ?, ?)'
    c.execute(insert_statement, (name, phone_number, num_rooms,
                                 room_type, days_staying, check_in, check_out))
    conn.commit()


def get_guest():
    guest_id = int(input('enter guest_id: '))
    guest = Guest(guest_id)
    print(guest.name)

def create_db_tables():
    conn = sqlite3.connect('hoteldb')
    c = conn.cursor()
    c.execute ('''CREATE TABLE hotels (hotel_id INTEGER PRIMARY KEY AUTOINCREMENT, hotel_name text NOT NULL)''')
    c.execute('''CREATE TABLE room_types (room_type INTEGER PRIMARY KEY, description text)''')
    c.execute ('''CREATE TABLE rooms (room_num INTEGER PRIMARY KEY, room_type INTEGER, rate INTEGER, availability INTEGER NULL DEFAULT 1,
                FOREIGN KEY (room_type) REFERENCES room_types (room_type))''')
    c.execute('''CREATE TABLE reservations (reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, guest_id INTEGER, room_num INTEGER, num_rooms INTEGER, room_type INTEGER, check_in DATETIME, check_out DATETIME,
                FOREIGN KEY (guest_id) REFERENCES guests ('phone_number'),
                FOREIGN KEY (room_num) REFERENCES rooms(room_num),
                FOREIGN KEY (room_type) REFERENCES room_types (room_type))''')
    c.execute ('''CREATE TABLE guests (phone_number INTEGER PRIMARY KEY UNIQUE, name VARCHAR(50), reservation_id INTEGER, hotel_id INTEGER,
            FOREIGN KEY (hotel_id) REFERENCES hotels (hotel_id),
            FOREIGN KEY (reservation_id) REFERENCES reservations (reservation_id))''')
    c.execute ('''CREATE TABLE cancellations (cancellation_id INTEGER PRIMARY KEY NOT NULL, guest_id INTEGER,
            FOREIGN KEY (guest_id) REFERENCES guests (phone_number))''')

def main(hn, tp):
    create_db_tables()
    while True:
        thing = input(
            'What do you want to do? \n 1. Create Hotel \n 2. Manage Guest \n 3. Exit \n\t')
        if int(thing) == 1:
            create_hotel()
        if int(thing) == 2:
            guest_thing = input('What do you want to do? \n 1. Create Guest, \n 2. Retrieve Guest \n 3. Exit \n\t')
            if int(guest_thing) == 1:
                create_guest()
            elif int(guest_thing) == 2:
                get_guest()
            elif int(guest_thing) == 3:
                break
        if int(thing) == 3:
            break

    hotel_obj = Hotel(hn, tp, guest_obj)
    total_cost = hotel_obj.t_cost()
    rooms_booked = hotel_obj.occupied()


def parse_args(arglist):
    parser = ArgumentParser()
    parser.add_argument("-hn", "--hotel_name", default='Random Hotel',
                        type=str, help="The name of the hotel")
    parser.add_argument("-tp", "--tax_perc", default=.1, type=float,
                        help="The amount of tax the hotel charges per transaction")
    # parser.add_argument("-n", "--name", type = str, help = "Enter your name")
    # parser.add_argument("-p", "--phone_number", type = str, help = "guests phone number")
    # parser.add_argument("-nr", "--num_rooms",type = int, help = "number of rooms you want to reserve")
    # parser.add_argument("-rt","--room_type", type = str, help = "room types: single, double, queen, king")
    # parser.add_argument("-ci", "--check_in", help = "enter check in date in 'YYYY/MM/DD' format")
    # parser.add_argument("-co", "--check_out", help = "enter check out date in 'YYYY/MM/DD' format")
    args = parser.parse_args(arglist)

    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(hn=args.hotel_name, tp=args.tax_perc)

