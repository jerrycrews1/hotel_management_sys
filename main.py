""" Hotel Management System.
"""


class Room:
    """ Represents a room.

    Attributes:
        rm_number (str): The room number.
        clearn (bool): True if the room is clean, else false.
                       Set to True by default.

    Args:
        rm_number (str): The room number.
        cost (float): The cost of the room.
    """

    def __init__(self, rm_number):
        self.rm_number = rm_number
        self.clearn = True


class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
        rooms (list of objs): The rooms belonging to the hotel.

    Args:
        name (str): The name of the hotel.
    """

    def __init__(self, name):
        self.name = name


class Reservation:
    """ Represents a hotel reservation.

    Attributes:
        hotel (obj): A hotel object.
        rooms (list of objs): List of room objects.
        guest (obj): The guest who is making the reservation.
        cost (float): The cost of the reservation.

    Args:
        hotel (obj): A hotel object.
        rooms (list of objs): List of room objects.
        guest (obj): The guest who is making the reservation.
    """

    def __init__(self, hotel, rooms, guest):
        self.hotel = hotel
        self.room = rooms
        self. guest = guest
