import sqlite3
import datetime
from datetime import date


class EarlyCheckInError(Exception):
    """Raised when an early check in is not approved."""
    pass


class EarlyCheckOutError(Exception):
    """Raised when an early check out is not approved."""
    pass


class Reservation:
    """ Represents a hotel reservation.

    Attributes:
        reservation_id (int): The reservation id.
        guest_id (int): The guest id.
        room_num (int): The room number.
        check_in (datetime): The date the guest will check in.
        check_out (datetime): The date the guest will check out.
        hotel_id (int): The id of the hotel.
    """

    def __init__(self, reservation_id):
        """ Initializes a Reservation object.

        Creates a reservation object from the reservation table in the DB.

        Side Effects:
            Sets the reservation_id, guest_id, check_in, check_out, cost, and the hotel_id attributes
            and calculates the cost of the reservation.
        """
        self.conn = sqlite3.connect('hotel.db')
        c = self.conn.cursor()
        c.execute('SELECT * FROM reservations WHERE reservation_id = ?',
                  (reservation_id, ))
        reservation = c.fetchone()

        self.reservation_id = reservation[0]
        self.guest_id = reservation[1]
        self.check_in = datetime.datetime.strptime(
            reservation[2], '%Y-%m-%d %H:%M:%S')
        self.check_out = datetime.datetime.strptime(
            reservation[3], '%Y-%m-%d %H:%M:%S')
        self.cost = float(reservation[4])
        self.hotel_id = reservation[5]

        # get the initial cost of the reservation upon creation.
        self.edit_cost()

    def edit_cost(self, amount=None, add=False):
        """ Edits the cost of the reservation.

        Goes through the rooms in the reservation and calculates the
        cost by the rate * the number of days of the reservation. 

        Args:
            amount (float): the amount to change the cost by.
            add (bool): Whether to credit the account or not. 

        Side Effects:
            Updates the cost attribute and updates the cost of the
            reservaiton in the DB.

        Returns:
            (float): The new cost of the reservation

        """
        c = self.conn.cursor()
        # If add is False, we subtract the amount
        if amount and not add:
            self.cost += amount
        # If add is true, we add (or credit) the user's reservation
        elif amount and add:
            self.cost -= amount
        # if amount isn't provided (at the beginning), and add is false (by default) calculate the amount of the reservation.
        else:
            query = f'''SELECT room_num, rate FROM rooms JOIN reservation_has_rooms ON (room_num = room_id) WHERE reservation_id = {self.reservation_id}'''
            c.execute(query)
            rooms = c.fetchall()
            num_days = self.check_out - self.check_in
            days = num_days.days + 1
            for room in rooms:
                self.cost += room[1] * days
            c = self.conn.cursor()
            query = 'UPDATE reservations SET cost = ? WHERE reservation_id = ? and hotel_id = ?'
            c.execute(query, (self.cost, self.reservation_id, self.hotel_id))
            self.conn.commit()
            return self.cost

    def edit_check_in(self, new_date):
        """ Edits the reservation check in date.

        Args:
            new_date (datetime): the new check in date.

        Side Effects:
            Changes the check in attribute and updates the check in
            element in the DB. Finally, it updates the cost of the
            reservation by calling the edit_cost method.

        """
        c = self.conn.cursor()
        # Get all rooms in the reservation.
        query = f'''SELECT * FROM reservation_has_rooms WHERE reservation_id = {self.reservation_id}'''
        c.execute(query)
        rooms = c.fetchall()
        new_check_in = new_date
        for room in rooms:
            # check each room to see if an early check in would interfere with someone else's late checkout.
            # Select the rooms from reservation_has_rooms table that don't belong to this reservation_id and check those to see if dates interfere
            query = f'''SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE reservation_id != {self.reservation_id} AND room_id = {room[0]} AND check_out >= "{new_check_in}"'''
            c.execute(query)
            rooms_available = c.fetchall()
            if len(rooms_available) > 0:
                raise EarlyCheckOutError(
                    'Unfortunately that interferes with another guest\'s check in. Please try again.')
        c.execute('UPDATE reservations SET check_in = ? WHERE reservation_id = ?',
                  (new_check_in, self.reservation_id))
        self.conn.commit()
        self.check_in = new_check_in
        self.edit_cost()

    def edit_check_out(self, new_date):
        """ Edits the reservation check in date.

        Args:
            new_date (datetime): the new check out date.

        Side Effects:
            Changes the check out attribute and updates the check out
            element in the DB. Finally, it updates the cost of the
            reservation by calling the edit_cost method.

        """
        c = self.conn.cursor()
        # Get all rooms in the reservation.
        query = f'''SELECT * FROM reservation_has_rooms WHERE reservation_id = {self.reservation_id}'''
        c.execute(query)
        rooms = c.fetchall()
        new_check_out = new_date
        for room in rooms:
            # check each room to see if an early check in would interfere with someone else's late checkout.
            # Select the rooms from reservation_has_rooms table that don't belong to this reservation_id and check those to see if dates interfere
            query = f'''SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE reservation_id != {self.reservation_id} AND room_id = {room[0]} AND check_in <= "{new_check_out}"'''
            c.execute(query)
            rooms_available = c.fetchall()
            if len(rooms_available) > 0:
                raise EarlyCheckOutError(
                    'Unfortunately that interferes with another guest\'s check in. Please try again.')
        c.execute('UPDATE reservations SET check_out = ? WHERE reservation_id = ?',
                  (new_check_out, self.reservation_id))
        self.conn.commit()
        self.check_out = new_check_out
        self.edit_cost()

        c.execute(
            'UPDATE reservations SET check_out = ? WHERE reservation_id = ?', (
                new_date, self.reservation_id))
        self.edit_cost()

    def late_checkout(self, hours):
        """ Gives the guest a late check out.

        Checks if giving the guest a late check out will interfere with
        another guest's reservation and updates the check out element of
        the reservation in the DB.

        Args:
            hours(int): The number of hours to add to the check out time.

        Side Effects:
            Modifies the check_out attribute by adding the hours to it and
            updates the check out time in the DB.

        Raises:
            EarlyCheckOutError: Raises if an early check out would interefere
                                with another guest's reservations.
        """
        c = self.conn.cursor()
        # Get all rooms in the reservation.
        query = f'''SELECT * FROM reservation_has_rooms WHERE reservation_id = {self.reservation_id}'''
        c.execute(query)
        rooms = c.fetchall()
        new_check_out = self.check_out + datetime.timedelta(hours=hours)
        for room in rooms:
            # check each room to see if an early check in would interfere with someone else's late checkout.
            # Select the rooms from reservation_has_rooms table that don't belong to this reservation_id and check those to see if dates interfere
            query = f'''SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE reservation_id != {self.reservation_id} AND room_id = {room[0]} AND check_in <= "{new_check_out}"'''
            c.execute(query)
            rooms_available = c.fetchall()
            if len(rooms_available) > 0:

                raise EarlyCheckOutError(
                    'Unfortunately that interferes with another guest\'s check in. Please try again.')
        c.execute('UPDATE reservations SET check_out = ? WHERE reservation_id = ?',
                  (new_check_out, self.reservation_id))
        self.conn.commit()
        self.check_out = new_check_out

    def early_checkin(self, hours):
        """ Gives the guest a early check in.

        Checks if giving the guest an early check in will interfere with
        another guest's reservation and updates the check in element of
        the reservation in the DB.

        Args:
            hours(int): The number of hours to subtract from the check in time.

        Side Effects:
            Modifies the check_in attribute by subtracting the hours from it and
            updates the check in time in the DB.

        Raises:
            EarlyCheckOutError: Raises if an early check out would interefere
                                with another guest's reservations.
        """
        c = self.conn.cursor()
        # Get all rooms in the reservation.

        query = f'''SELECT * FROM reservation_has_rooms WHERE reservation_id = {self.reservation_id}'''
        c.execute(query)
        rooms = c.fetchall()
        new_check_in = self.check_in - datetime.timedelta(hours=hours)
        for room in rooms:

            # check each room to see if an early check in would interfere with someone else's late checkout.
            # Select the rooms from reservation_has_rooms table that don't belong to this reservation_id and check those to see if dates interfere
            query = f'''SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE reservation_id != {self.reservation_id} AND room_id = {room[0]} AND check_out >= "{new_check_in}"'''
            c.execute(query)
            rooms_available = c.fetchall()
            if len(rooms_available) > 0:

                raise EarlyCheckInError(
                    'Unfortunately that interferes with another guest\'s checkout. Please try again.')
        c.execute('UPDATE reservations SET check_in = ? WHERE reservation_id = ?',
                  (new_check_in, self.reservation_id))
        self.conn.commit()
        self.check_in = new_check_in
