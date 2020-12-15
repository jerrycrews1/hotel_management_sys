""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys

import sqlite3


class Room:
    """ Represents a room.

    Attributes:
        rm_number (str): The room number.
        clean (bool): True if the room is clean, else false.
                      Set to True by default.
        cost (float): The cost of the room.
        type (str): The type of room (double, king, etc).
        occupied (bool): True if room is occupied, else False.
                         Set to False by default.
        handicap (bool): True if room is handicap accessible, else False.
    """

    def __init__(self, rm_number, type, handicap):
        """ Initializes a Room object.

        Args:
            rm_number (str): The room number.
            type (str): The type of room (double, king, etc).
            handicap (bool): Whether a room is handicap accessible or not.

        Side Effects:
            Sets the rm_number, clean, cost, type, and occupied attributes.
        """
        self.rm_number = rm_number
        self.clean = True
        self.occupied = False
        self.type = str()
        self.cost = float()
        
        if self.type == 'single':
            self.cost = 90
        elif self.type == 'double':
            self.cost = 100
        elif self.type == 'queen':
            self.cost = 110
        elif self.type == 'king':
            self.cost = 120


class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
        
    """

    def __init__(self, name, tax_perc):
        """ Initializes a Hotel object.

        Args:
            name (str): The name of the hotel.
            tax_perc (float): The tax percentage the hotel is subject to.

        Side Effects:
            Sets the name, rooms, and tax_perc attribute attributes.
        """
        self.name = name
        rooms = list()
        self.tax_perc = tax_perc

        room_list = [x for x in range(1, 21)]
        roomtype = ['single', 'double', 'queen', 'king']
        for num in room_list:
            if num <= 5:
                rooms.append(Room(str(num), roomtype[0], True))
            elif 6 <= num <= 10:
                rooms.append(Room(str(num), roomtype[1], False))
            elif 11 <= num <= 15:
                rooms.append(Room(str(num), roomtype[2], False))
            elif 14 <= num <= 20:
                rooms.append(Room(str(num), roomtype[3], False))
            
class Reservation:
    """ Represents a hotel reservation.
    Attributes:
        hotel (obj): A hotel object.
        rooms (list of objs): List of room objects.
        guest (obj): The guest who is making the reservation.
        cost (float): The cost of the reservation.
        check_in_date (datetime): The date the guest will check in.
        check_out_date (datetime): The date the guest will check out.
    """

    def __init__(self, hotel, rooms, guest, check_in_date_time, check_out_date_time):
        """ Initializes a Reservation object.

        Args:
            hotel (obj): A hotel object.
            rooms (list of objs): List of room objects.
            guest (obj): The guest who is making the reservation.
            check_in_date_time (datetime): The date the guest will check in.
            check_out_date_time (datetime): The date the guest will check out.
            conn (obj): A connection object of a sqlite db.

        Side Effects:
            Sets the hotel, rooms, guest, check_in_date_time, and the check_out_date_time attributes
            and connects to the reservation's table in the sqlite database.
        """

        self.hotel = Hotel()
        self.rooms = rooms
        self.guest = Guest()
        self.check_in_date_time = check_in_date_time
        self.check_out_date_time = check_out_date_time

    def __repr__(self):
        return f"Reservation({repr(self.hotel)}, {[repr(room) for room in self.rooms]}, \
            {repr(self.check_in_date_time)}, {repr(self.check_out_date_time)})"

    def __str__(self):
        return f"Reservation for {self.guest.name} checking into {self.hotel.name} on {self.check_in_date_time} \
            and checking out on {self.check_out_date_time}"
    

    def check_in(self):
        """ Checks in the guest to the hotel.

        Side Effects:
            Changes the room object's clean attribute to False.
            Changes the room object's occupied attribute to True.

        """
        pass

    def check_out(self):
        """ Checks out the guest from the hotel.

        Side Effects:
            Changes the room object's occupied attribute to False.
        """
        pass

    def late_checkout(self, hours):
        """ Gives the guest a late checkout.

        This method checks if the guest already has a late checkout
        and if they don't, adds the hours to the checkout time.

        Args:
            hours(int): The number of hours to add to the checkout time.

        Side Effects:
            Modifies the check_out_date_time attribute by adding the hours to it.

        Returns:
            (datetime): The new checkout date and time.
        """
        pass

    def early_checkin(self, hours):
        """ Gives the guest an early checkin.

        This method checks if an early checkin has already been given.  It then
        checks to ensure that giving an early checkin doesn't interfere with another
        reservation.

        Args:
            hours(int): The number of hours to subtract from the checkin time.

        Side Effects:
            Modifies the check_in_date_time attribute by stubtracting hours from it.

        Returns:
            (datetime): The new checkin time.
        """
        pass
    
    def clean_room(self):
        """ Confirms that a room that was occupied is now clean.
        
        Side Effects:
            Changes the room object's clean attribute to True.
        """
        pass


class Guest:
    """ Represents a Guest. 

    Attributes:
        name (str): guests name
        email (str): guests email
        phone_number (str): guests phone number

    Args:
        name (str): guests name
        email (str): guests email
        phone_number (str): guests phone number
    """

    def __init__(self, name, email, phone_number):
        """ Gathers basic information about guest.

        This method will ask user to input information about themselves.

        Args:
            name (str): guests name
            email (str): guests email
            phone_number (str): guests phone number

        Side Effects:
            Sets the name, email, and phone_number attributes.
        """

        self.name = name
        self.address = email
        self.phone_number = phone_number
        
def main(hn, tp):

    hotel_obj = Hotel(hn,tp)
    print(hotel_obj.tax_perc)
    # x = input("what's up")
    # print(x)
    # [Guest name,[{0:single, 1:queen}]]
    
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
    main(hn=args.hotel_name, tp = args.tax_perc)
