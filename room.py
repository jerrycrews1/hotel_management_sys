import sqlite3


class Room:
    """ Represents a room.

    Attributes:
        rm_number (str): The room number.
        availability (int): 1 if the room is clean, else 2.
                      Set to 1 by default.
        rate (float): The cost of the room.
    """

    def __init__(self, room_number):
        """ Initializes a Room object from the rooms table in the db.

        Args:
            room_number (int): The room number.

        Side Effects:
            Sets the room_number, availability, room_type_id, and rate attributes.
        """
        self.conn = sqlite3.connect('hotel.db')
        c = self.conn.cursor()

        c.execute('SELECT * FROM rooms WHERE room_number = ?', (room_number, ))
        room = c.fetchone()

        self.room_number = room[0]
        self.room_type_id = room[1]
        self.rate = room[2]
        self.availability = room[3]
