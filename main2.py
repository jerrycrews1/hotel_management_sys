""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
import sys
import datetime
import sqlite3
from room import Room
from guest import Guest
from hotel import Hotel
from reservation import Reservation
from create_db import create_db_tables, create_room_types, create_rooms


def get_avialable_rooms_by_date(new_check_in, new_check_out, num_rooms=1):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    query = f'''SELECT room_num FROM rooms WHERE room_num NOT IN (SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE check_in <= '{new_check_in}' OR '{new_check_in}' < check_out OR '{new_check_in}' <= check_in OR '{new_check_in}' < check_out OR check_in <= '{new_check_out}' OR '{new_check_out}' < check_out OR '{new_check_out}' <= check_out OR check_out < '{new_check_out}')'''
    c.execute(query)
    rooms_available = c.fetchall()
    return rooms_available


def get_available_rooms_by_type(room_type):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    query = f'''SELECT room_num FROM rooms WHERE room_type_id = (SELECT room_type_id FROM room_types WHERE description = '{room_type}') ;'''
    c.execute(query)
    rooms_available = c.fetchall()
    return rooms_available


def create_guest(name=None, phone_number=None):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    if not name:
        name = input("Enter the guest's name >").title()
    if not phone_number:
        phone_number = input("Enter the guest's phone_number >")
    while True:
        # Check if user with that phone number already exists
        try:
            get_guest(phone_number)
            print('Guest with this phone number already exists. Please try again.')
            phone_number = input("Enter the guest's phone_number >")
        except TypeError:
            break

    insert_statement = 'INSERT INTO guests(name, phone_number) VALUES(?, ?)'
    c.execute(insert_statement, (name, phone_number))
    conn.commit()
    c.execute('SELECT * FROM guests ORDER BY guest_id DESC LIMIT 1')
    guest_phone_number = c.fetchone()[1]
    guest = Guest(guest_phone_number)
    print('Guest created successfully.')
    return guest


def get_guest(phone_number=None):
    if not phone_number:
        phone_number = int(input('Enter guest\'s phone number >'))
    guest = Guest(phone_number)
    return guest


def edit_guest():
    guest = get_guest()
    to_edit = int(
        input("What do you want to edit? \n1. Phone Number, \n2. Name\n>"))
    if to_edit == 1:
        new_number = input("Please enter a new phone number (3323449506) >")
        # NEED TO CHECK IF NEW PHONE NUMBER ALREADY EXISTS
        guest.edit_phone_number(new_number)
    elif to_edit == 2:
        new_name = input("Please enter a new name >")
        guest.edit_name(new_name)


def create_hotel():
    tax_perc = float(input('Enter the hotel tax percentage (0.1 for 10%) >'))
    name = input("Enter the name of the hotel >")
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()

    insert_statement = (
        'INSERT INTO hotels(hotel_name, tax_perc) VALUES(?, ?)')
    c.execute(insert_statement, (name, tax_perc))
    conn.commit()

    c.execute('SELECT * FROM hotels ORDER BY hotel_id DESC LIMIT 1')
    hotel_id = c.fetchone()[0]
    hotel = Hotel(hotel_id)
    print(hotel)
    return hotel


def get_hotel():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c.execute('SELECT * FROM hotels')
    hotels = c.fetchall()
    if len(hotels) < 1:
        print('Sorry, there are no hotels in the system. Please create one now')
        return create_hotel()
    for index, hotel in enumerate(hotels):
        print(f'{index + 1}: {hotel[1]}')
    hotel_id = int(input('Which hotel do you want to manage? >'))
    hotel = Hotel(hotel_id)
    return hotel


def create_reservation(hotel_id):
    ''' Creates a new reservation

    Returns:
        reservation (obj): A reservation object.
    '''
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    while True:
        phone_number = int(input('Enter guest\'s phone number >'))
        try:
            # If the guest doesn't already exist, move to the except statement.
            guest = get_guest(phone_number=phone_number)
            break
        except TypeError:
            new_guest_thing = int(input(
                f'That guest doesn\'t exists. Would you like to create a new guest using the phone number you entered: {phone_number}?\n1. Yes\n2. No(use different phone number)\n>'))
            if new_guest_thing == 1:
                # Create a new guest from the phone_number already entered.
                guest = create_guest(phone_number=phone_number)
                break
            elif new_guest_thing == 2:
                continue
    guest_id = guest.guest_id

    while True:
        # Get the user's check_in date, change to a datetime
        check_in = input('Enter your check in date (Jun 10 2020): ')
        check_in = datetime.datetime.strptime(check_in, '%b %d %Y')
        check_in = check_in.replace(hour=13, minute=00)
        # Get the number of days stating and create the check_out datetime from that
        days_staying = int(input("Enter how many days the guest be staying >"))
        check_out = (check_in + datetime.timedelta(days=days_staying))
        check_out = check_out.replace(hour=11, minute=00)

        num_rooms = int(
            int(input("Enter how many rooms the guest needs (no more than 5) >")))

        rooms = list()
        # Get the rooms that are available on those dates
        rooms_avialable_on_dates = get_avialable_rooms_by_date(
            check_in, check_out, num_rooms)
        # If there are rooms, proceed.
        if len(rooms_avialable_on_dates) >= num_rooms:
            # Loop through each room the user wants and check if the type is available.
            for room in range(num_rooms):
                while True:
                    room_type = input(
                        f"Enter the type of room #{room + 1} the guest wants (king, queen, double, single) >").casefold()
                    # Get the rooms that are availabe of this type
                    rooms_avialable_by_type = get_available_rooms_by_type(
                        room_type)
                    # Make a set of rooms which are available on those dates AND by that type
                    rooms = (set(rooms_avialable_on_dates) &
                             set(rooms_avialable_by_type))
                    # If there are rooms, proceed, else try again.
                    if len(rooms) > 0:
                        break
                    else:
                        print(
                            'Sorry there are no available rooms of that type on the dates you entered.')
                        continue

            # Add the reservation to the db
            insert_statement = 'INSERT INTO reservations (guest_id, check_in, check_out, hotel_id) VALUES (?, ?, ?, ?)'
            c.execute(insert_statement, (guest_id,
                                         check_in, check_out, hotel_id))
            conn.commit()
            # Get the reservation back from the db
            c.execute(
                f'''SELECT * FROM reservations WHERE hotel_id = {hotel_id} ORDER BY reservation_id  DESC LIMIT 1''')
            reservation_id = c.fetchone()[0]
            # Loop through each room the user wants and add it to the reservation_has_rooms table in the db.
            rooms = list(rooms)[-num_rooms:]
            for room in rooms:
                res_to_rooms_insert = 'INSERT INTO reservation_has_rooms VALUES (?, ?)'
                c.execute(res_to_rooms_insert,
                          (reservation_id, room[0]))
            conn.commit()
            reservation = Reservation(reservation_id)
            break
        elif len(rooms_avialable_on_dates) < num_rooms:
            print("Sorry! Those rooms aren't available for those dates.")
            continue
        else:
            continue
    print(
        f'Your reservation has been created, thank you {guest.name}. The cost is ${reservation.cost}.')
    return reservation


def get_reservation(reservation_id, hotel_id):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    query = '''SELECT * FROM reservations WHERE reservation_id = ? AND hotel_id = ?'''
    try:
        c.execute(query, (reservation_id, hotel_id))
        reservation = c.fetchone()
        return reservation
    except TypeError:
        return 'Sorry, that reservation wasn\'t found'


def get_reservations(hotel_id):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    while True:
        phone_number = int(input('Enter guest\'s phone number >'))
        try:
            # If the guest doesn't already exist, move to the except statement.
            get_guest(phone_number=phone_number)
            break
        except TypeError:
            print('No reservation under that phone number were found.')
            continue

    query = 'SELECT * FROM reservations WHERE guest_id = (SELECT guest_id FROM guests WHERE phone_number = ?) AND hotel_id = ?;'
    c.execute(query, (phone_number, hotel_id))
    # Print the reservations for the specific guests and have them select which reservation by id.
    reservations = c.fetchall()
    for reservation in reservations:
        print(
            f'{reservation[0]}: Check In: {reservation[2]} Check Out {reservation[3]}')
    return reservations


def edit_reservation(hotel_id):
    get_reservations(hotel_id)
    reservation_id = int(input('Which reservation do you want to manage? >'))
    try:
        reservation = get_reservation(reservation_id, hotel_id)
        reservation = Reservation(reservation[0])
    except TypeError:
        print('Sorry that reservation could not be found.')
    reservation_edit = int(input(
        'Which part of the reservation do you want to edit?\n1. Check In Date, \n2. Check Out Date, \n3. Early Check In \n4. Late Check Out\n5. Cancel Reservation\n>'))
    if reservation_edit == 1:
        check_in = input('Enter your check in date (Jun 10 2020): ')
        check_in = datetime.datetime.strptime(check_in, '%b %d %Y')
        check_in = check_in.replace(hour=13, minute=00)
        reservation.edit_check_in(check_in)
    elif reservation_edit == 2:
        # Get the number of days stating and create the check_out datetime from that
        days_staying = int(input("Enter how many days the guest be staying >"))
        check_in = reservation.check_in
        check_out = (reservation.check_in +
                     datetime.timedelta(days=days_staying))
        reservation.edit_check_out(check_out)
    elif reservation_edit == 3:
        while True:
            hours = int(input(
                'How many hours early would you like to check in? No more than 2 hours allowed. >'))
            if hours > 2:
                continue
            try:
                reservation.early_checkin(hours)
                print('Your early check in has been approved.')
                break
            except:
                continue
    elif reservation_edit == 4:
        while True:
            hours = int(input(
                'How many hours late would you like to check out? No more than 2 hours is allowed. >'))
            if hours > 2:
                continue
            try:
                reservation.late_checkout(hours)
                print('Your late check out has been approved.')
                break
            except:
                continue


def cancel_reservation(hotel_id):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    while True:
        get_reservations(hotel_id)
        reservation_id = int(
            input('Which reservation do you want to manage? >'))
        try:
            reservation = get_reservation(reservation_id, hotel_id)
            reservation = Reservation(reservation[0])
            # Delete the reservation from the reservation has rooms table first to prevent orphan record.
            delete_res_to_rooms_query = f'''DELETE FROM reservation_has_rooms WHERE reservation_id = {reservation.reservation_id} '''
            c.execute(delete_res_to_rooms_query)
            # Delete the reservation from the reservation table.
            delte_res_query = f'''DELETE FROM reservations WHERE reservation_id = {reservation.reservation_id} AND hotel_id = {hotel_id}'''
            c.execute(delte_res_query)
            insert_into_cancellations_query = f'INSERT INTO cancellations(reservation_id) VALUES({reservation.reservation_id})'
            c.execute(insert_into_cancellations_query)
            conn.commit()
            break
        except TypeError:
            print('Sorry that reservation could not be found.')
            continue
    print('Reservation deleted')
    return


def main():
    # create_db_tables()
    # create_room_types()
    # create_rooms()
    print('Welcome to the Hotel Management System.')
    hotel_thing = input(
        'Which are you doing? \n0. Exit\n1. Managing an Existing Hotel, or \n2. Creating a New Hotel? \n>')
    if int(hotel_thing) == 1:
        while True:
            try:
                hotel = get_hotel()
                break
            except:
                print('Sorry that wans\'t an option. Please try again.')
                continue
    elif int(hotel_thing) == 2:
        hotel = create_hotel()
    else:
        return
    hotel_id = hotel.hotel_id
    print(f'We are managing the {hotel.name} hotel.')
    while True:
        thing = input(
            'What do you want to do? \n0. Back\n1. Manage Guest \n2. Manage Reservation \n3. OTHER (TBD) \n>')
        if int(thing) == 1:
            guest_thing = input(
                'What do you want to do? \n0. Back\n1. Create Guest, \n2. Retrieve Guest \n3. Edit Guest Information \n>')
            if int(guest_thing) == 1:
                create_guest()
            elif int(guest_thing) == 2:
                while True:
                    try:
                        guest = get_guest()
                        break
                    except TypeError:
                        print('Sorry, that guest could not be found.')
                        continue
                print(f'Name: {guest.name}\nPhone: {guest.phone_number}')
            elif int(guest_thing) == 3:
                edit_guest()
            else:
                continue
        elif int(thing) == 2:
            reservation_thing = input(
                'What do you want to do? \n0. Back\n1. New Reservation, \n2. View Reservation, \n3. Edit An Existing Reservation, \n4. Cancel Reservation\n>')
            if int(reservation_thing) == 1:
                create_reservation(hotel_id)
            elif int(reservation_thing) == 2:
                get_reservations(hotel_id)
            elif int(reservation_thing) == 3:
                edit_reservation(hotel_id)
            elif int(reservation_thing) == 4:
                cancel_reservation(hotel_id)
            else:
                break
        elif int(thing) == 3:
            pass
        else:
            break


if __name__ == "__main__":
    main()
