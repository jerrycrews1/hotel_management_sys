import sqlite3


class Reservation:
    """ Represents a hotel reservation.

    Attributes:
        reservation_id (int): The reservation id.
        guest_id (int): The guest id.
        room_num (int): The room number.
        check_in (datetime): The date the guest will check in.
        check_out (datetime): The date the guest will check out.
    """

    def __init__(self, reservation_id):
        """ Initializes a Reservation object.

        Side Effects:
            Sets the hotel, rooms, guest, check_in, and the check_out attributes
            and connects to the reservation's table in the sqlite database.
        """
        self.conn = sqlite3.connect('hotel.db')
        c = self.conn.cursor()
        c.execute('SELECT * FROM reservations WHERE reservation_id = ?',
                  (reservation_id, ))
        reservation = c.fetchone()
        print(reservation)

        self.reservation_id = reservation[0]
        self.guest_id = reservation[1]
        self.check_in = reservation[2]
        self.check_out = reservation[3]

    def edit_check_in(self, new_date):
        """ Edits the reservation check in date.

        Side Effects:
            Changes the check in attribute.
        """
        c = self.conn.cursor()
        try:
            c.execute(
                'UPDATE reservations SET check_in = ? WHERE reservation_id = ?', (
                    self.reservation_id, new_date))
            self.check_in = new_date
        except TypeError:
            return 'Could not edit the reservation.'

    def edit_check_out(self, new_date):
        """ Edits the reservation check in date.

        Side Effects:
            Changes the check in attribute.
        """
        c = self.conn.cursor()
        try:
            c.execute(
                'UPDATE reservations SET check_out = ? WHERE reservation_id = ?', (
                    self.reservation_id, new_date))
            self.check_out = new_date
        except TypeError:
            return 'No Reservation with this id found.'

    def late_checkout(self, hours):
        """ Gives the guest a late checkout.

        This method checks if the guest already has a late checkout
        and if they don't, adds the hours to the checkout time.

        Args:
            hours(int): The number of hours to add to the checkout time.

        Side Effects:
            Modifies the check_out attribute by adding the hours to it.

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
