""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys

class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
        
    """

    def __init__(self, name, tax_perc): # I, Samson, removed the attribute 'rooms' for the parse args func to work. 
                                        # I could add another argument in the parse func instead, but I am not sure if that is necessary. If it is we can do so.

        """ Initializes a Hotel object.

        Args:
            name (str): The name of the hotel.
            tax_perc (float): The tax percentage the hotel is subject to.
            rooms (list of objs): The rooms belonging to the hotel.

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
    parser.add_argument("-hn", "--hotel_name", default='Random Hotel', type=str, help="The name of the hotel")
    parser.add_argument("-tp", "--tax_perc", default =.1, type=float, help="The amount of tax the hotel charges per transaction" )
    args = parser.parse_args(arglist)
    
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(hn=args.hotel_name, tp = args.tax_perc)