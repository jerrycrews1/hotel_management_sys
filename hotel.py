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

        room_list = [x for x in range(1, 21)]
        roomtype = ['single', 'double', 'queen', 'king']
        self.rooms_dict = {}
        self.occupied_rooms = {}

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
            # + ((90*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (90*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        elif self.guest_obj.room_type == 'double':
            # + ((100*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (100*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        elif self.guest_obj.room_type == 'queen':
            # + ((110*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (110*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        elif self.guest_obj.room_type == 'king':
            # + ((120*self.guest_obj.num_rooms)*self.tax_perc)
            cost = (120*self.guest_obj.num_rooms) * self.guest_obj.days_staying
        cost = cost + (cost*self.tax_perc)
        print(f"{self.guest_obj.name}'s total cost is ${cost:.2f}")

    def occupied(self):
        """
        Uses room type and number of rooms specified by guests to mark rooms as occupied and remove them from the available rooms to choose from.
        If too many rooms are attempting to be booked the method tells the user that there aren't enough rooms available.

        Return:
            possible_rooms (list): a list of available rooms

        """
        possible_rooms = []
        x = 0
        for key, value in self.rooms_dict.items():
            if self.room_type == value:
                possible_rooms.append(key)
        if len(possible_rooms) < self.num_rooms:
            print("Not enough rooms are available.")
        else:
            while x < self.num_rooms:
                self.occupied_rooms[possible_rooms[x]
                                    ] = self.rooms_dict.pop(possible_rooms[x])
                print("Room "+str(possible_rooms[x])+" is now booked.")
                x = x+1
        return possible_rooms
