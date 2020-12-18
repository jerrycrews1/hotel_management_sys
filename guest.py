import sqlite3


class Guest:
    """ Represents a Guest from the DB. 

    Attributes:
        guest_id (int): The guest id from the DB.
        phone_number (str): The guest's phone number.
        name (str): The guest's name.
    """

    def __init__(self, phone_number, database):
        """ Creates a guest object from the database.

        Args:
            phone_number (str): The guest's phone number.
            database (str): The database to connect to.

        Side Effects:
            Sets the guest_id, name, and phone_number attributes.
        """

        print(database)
        self.conn = sqlite3.connect(database)
        c = self.conn.cursor()
        c.execute('SELECT * FROM guests WHERE phone_number = ?',
                  (phone_number, ))
        guest = c.fetchone()

        self.guest_id = guest[0]
        self.name = guest[2]
        self.phone_number = guest[1]

    def edit_phone_number(self, new_number):
        """ Changes the guest's phone number.

        Args:
            new_number (int): The new phone number.

        Side Effects:
            Updates the phone_number attribute and updates the phone
            number in the DB.
        """
        self.phone_number = new_number
        c = self.conn.cursor()
        c.execute('UPDATE guests SET phone_number = ? WHERE guest_id = ?',
                  (self.phone_number, self.guest_id))
        self.conn.commit()

    def edit_name(self, new_name):
        """ Changes the guest's name.

        Args:
            new_name (str): The new name.

        Side Effects:
            Updates the name attribute and updates the name in the DB.
        """
        self.name = new_name
        c = self.conn.cursor()
        c.execute('UPDATE guests SET new_name = ? WHERE guest_id = ?',
                  (self.name, self.guest_id))
        self.conn.commit()
