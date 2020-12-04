""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys
import datetime


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

        self.name = name
        self.tax_perc = tax_perc
        
        
        self.room_type=guest_obj.room_type
        self.num_rooms=guest_obj.num_rooms
        self.guest_obj=guest_obj
        
        
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
                
    def t_cost(self):
        """ This method calculates the total cost per reservation
        Return:
            cost(float): The total cost, including tax
        """
        
        if self.guest_obj.room_type == 'single':
            cost = (90*self.guest_obj.num_rooms) * self.guest_obj.days_staying  #+ ((90*self.guest_obj.num_rooms)*self.tax_perc)
        elif self.guest_obj.room_type == 'double':
            cost = (100*self.guest_obj.num_rooms) * self.guest_obj.days_staying #+ ((100*self.guest_obj.num_rooms)*self.tax_perc)
        elif self.guest_obj.room_type == 'queen':
            cost = (110*self.guest_obj.num_rooms) * self.guest_obj.days_staying #+ ((110*self.guest_obj.num_rooms)*self.tax_perc)
        elif self.guest_obj.room_type == 'king':
            cost = (120*self.guest_obj.num_rooms) * self.guest_obj.days_staying #+ ((120*self.guest_obj.num_rooms)*self.tax_perc)
        cost = cost + (cost*self.tax_perc)
        print(f"{self.guest_obj.name}'s total cost is ${cost:.2f}")
        
    def occupied(self):
        """
        Uses room type and number of rooms specified by guests to mark rooms as occupied and remove them from the available rooms to choose from.
        If too many rooms are attempting to be booked the method tells the user that there aren't enough rooms available.
        """
        possible_rooms=[]
        x=0
        for key, value in self.rooms_dict.items():
            if self.room_type == value: 
                possible_rooms.append(key)
        if len(possible_rooms)<self.num_rooms:
            print ("Not enough rooms are available.")
        else:
            while x<self.num_rooms:
                self.occupied_rooms[possible_rooms[x]]=self.rooms_dict.pop(possible_rooms[x])
                print("Room "+str(possible_rooms[x])+" is now booked.")
                x=x+1
        return possible_rooms
                
class Guest:
    """ Represents a Guest. 

    Attributes:
        name (str): guests name
        phone_number (str): guests phone number
        num_rooms (int): number of rooms guest wants to book
        room_type (str): king, queen, double, single
        days_staying (int): number of days guest wants to stay
        check_in (datetime): date guest checks in
        check_out (datetime): date guest checks out

    Args:
        name (str): guests name
        phone_number (str): guests phone number
        num_rooms (int): number of rooms guest wants to book
        room_type (str): king, queen, double, single
        days_staying (int): number of days guest wants to stay
        check_in (datetime): date guest checks in
        check_out (datetime): date guest checks out
    """

    def __init__(self, name, phone_number, num_rooms, room_type, days_staying, check_in, check_out):
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
        self.days_staying = days_staying
        self.check_in = check_in
        self.check_out = check_out
        
def main(hn, tp):
 
    name = input("Enter the guest's name: ").capitalize()
    phone_number = input("Enter the guest's phone_number: ")
    num_rooms = int(input("Enter how many rooms the guest needs: "))
    room_type = input("Enter the type of room the guest wants (king, queen, double, single): ").casefold()
    check_in = datetime.date.today()
    days_staying = int(input("Enter how many days the guest be staying: " ))
    
    check_out = (check_in + datetime.timedelta(days=days_staying))
    
    guest_obj = Guest(name, phone_number, num_rooms, room_type, days_staying, check_in, check_out)
    hotel_obj = Hotel(hn,tp, guest_obj)
    total_cost=hotel_obj.t_cost()
    rooms_booked=hotel_obj.occupied()
    
    
    
    
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