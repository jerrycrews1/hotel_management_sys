""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys
import datetime

roomtype = ['single', 'double', 'queen', 'king']

class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
        
    """

    def __init__(self, name, tax_perc, guest_obj): 

        """ Initializes a Hotel object.

        Args:
            name (str): The name of the hotel.
            tax_perc (float): The tax percentage the hotel is subject to.

        Side Effects:
            Sets the name, and tax_perc attribute attributes.
        """
        print(guest_obj.name)
        self.name = name

        self.tax_perc = tax_perc
        
        self.room_type=guest_obj.room_type
        self.num_rooms=guest_obj.num_rooms

        room_list = [x for x in range(1, 21)]
        roomtype = ['single', 'double', 'queen', 'king']
        self.rooms_dict = {}
        self.occupied_rooms={}

        for num in room_list:
            if num <= 5:
                self.rooms_dict[num] = roomtype[0]
            elif 6 <= num <= 10:
                self.rooms_dict[num] = roomtype[1]
            elif 11 <= num <= 15:
                self.rooms_dict[num] = roomtype[2]
            elif 14 <= num <= 20:
                self.rooms_dict[num] = roomtype[3]
    def occupied(self):
        """
        Uses room type and number of rooms specified by guests to mark rooms as occupied and remove them from the available rooms to choose from.
        If too many rooms are attempting to be booked the method tells the user that there aren't enough rooms available.
        """
        possible_rooms=[]
        for key, value in self.rooms_dict.items():
            if self.room_type == value: 
                possible_rooms.append(key)
        if len(possible_rooms)<self.num_rooms:
            return "Not enough rooms are available."
        else:
            for rooms in self.num_rooms:
                x=0
                self.occupied_rooms[possible_rooms[x]]=self.rooms_dict.pop(possible_rooms[x])
                x=x+1
                
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

    def __init__(self, name, phone_number, num_rooms, room_type, check_in, check_out):
        """ Gathers basic information about guest, the room type they want and their check in and check out dates.

        Args:
            name (str): guests name
            phone_number (str): guests phone number
            num_rooms (int): number of rooms guest wants to reserve
            room_type (str): room type (single, double, queen, king)
            check_in (datetime): date guest checks in
            check_out (datetime): date guest wants to check out

        Side Effects:
            Sets the name, phone_number, num_rooms, room_type, check_in, check_out attributes.
        """

        self.name = name
        self.phone_number = phone_number
        self.num_rooms = num_rooms
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out
        
def main(hn, tp):
 
    name = input("Enter the guest's name: ")
    phone_number = input("Enter the guest's phone_number: ")
    num_rooms = int(input("Enter how many rooms the guest needs: "))
    room_type = input("Enter the type of room the guest wants: (king, queen, double, single) ")
    check_in = datetime.date.today()
    days_staying = int(input("Enter how many days the guest be staying: " ))
    
    check_out = (check_in + datetime.timedelta(days=days_staying))
    
    guest_obj = Guest(name, phone_number, num_rooms, room_type, check_in, check_out)
    hotel_obj = Hotel(hn,tp, guest_obj)

def parse_args(arglist):
    parser = ArgumentParser()
    parser.add_argument("-hn", "--hotel_name", default='Random Hotel', type=str, help="The name of the hotel")
    parser.add_argument("-tp", "--tax_perc", default =.1, type=float, help="The amount of tax the hotel charges per transaction" )
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