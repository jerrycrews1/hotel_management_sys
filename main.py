""" Hotel Management System.
"""


class Room:
    """ Represents a room.

    Attributes:
        rm_number (str): The room number.
        clean (bool): True if the room is clean, else false.
                       Set to True by default.
        cost (float): The cost of the room.

    Args:
        rm_number (str): The room number.
    """

    def __init__(self, rm_number):
        self.rm_number = rm_number
        self.clean = True


class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
        rooms (list of objs): The rooms belonging to the hotel.

    Args:
        name (str): The name of the hotel.
    """

    def __init__(self, name, tax_perc, rooms):
        self.name = name
        self.rooms={}
        self.tax_perc=tax_perc

        room_list = [x for x in range(1,21)] 
        roomtype=['single', 'double', 'queen', 'king']
        for num in room_list:
            if num <=5 :
                self.rooms.update({num:roomtype[0]})
            elif 6<=num <=10:
                self.rooms.update({num:roomtype[1]})
            elif 11<=num <=15:
                self.rooms.update({num:roomtype[2]})
            elif 14<=num <=20:
                self.rooms.update({num:roomtype[3]})
    


class Reservation:
    """ Represents a hotel reservation.

    Attributes:
        hotel (obj): A hotel object.
        rooms (list of objs): List of room objects.
        guest (obj): The guest who is making the reservation.
        cost (float): The cost of the reservation.
        check_in_date (datetime): The date the guest will check in.
        check_out_date (datetime): The date the guest will check out.

    Args:
        hotel (obj): A hotel object.
        rooms (list of objs): List of room objects.
        guest (obj): The guest who is making the reservation.
        check_in_date_time (datetime): The date the guest will check in.
        check_out_date_time (datetime): The date the guest will check out.
    """

    def __init__(self, hotel, rooms, guest, check_in_date_time, check_out_date_time):
        self.hotel = hotel
        self.room = rooms
        self.guest = guest
        self.check_in_date_time = check_in_date_time
        self.check_out_date_time = check_out_date_time

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
            hours (int): The number of hours to add to the checkout time.

        Side Effects:
            Modifies the check_out_date_time attribute by adding the hours to it.

        Returns:
            Returns the new checkout time.
        """
        pass
