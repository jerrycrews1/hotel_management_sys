import sqlite3


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
