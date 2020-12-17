import sqlite3


class Hotel:
    """ Represents the hotel that will be managed.

    Attributes:
        hotel_id (int): The hotel id.
        hotel_name (str): The name of the hotel.
        tax_perc (float): The tax percentage the hotel is subject to.
    """

    def __init__(self, hotel_id):
        """ Initializes a Hotel object.

        Args:
            hotel_id (int): The hotel id.

        Side Effects:
            Sets the name and tax_perc attribute attributes.
        """
        self.conn = sqlite3.connect('hotel.db')
        c = self.conn.cursor()
        c.execute('SELECT * FROM hotels WHERE hotel_id = ?',
                  (hotel_id, ))
        hotel = c.fetchone()

        self.hotel_id = hotel[0]
        self.name = hotel[1]
        self.tax_perc = hotel[2]
