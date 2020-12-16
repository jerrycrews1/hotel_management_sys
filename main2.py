""" Hotel Management System.

This module allows a hotel receptionist or manager to perform various functions
necessary for operating a hotel.
"""
from argparse import ArgumentParser
import sys
import datetime
import sqlite3
from guest import Guest
from hotel import Hotel
from room import Room
from reservation import Reservation
from create_db import create_db_tables, create_room_types, create_rooms


def create_guest(name=None, phone_number=None):
    if not name:
        name = input("Enter the guest's name: ").capitalize()
    if not phone_number:
        phone_number = input("Enter the guest's phone_number: ")

    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    insert_statement = 'INSERT INTO guests(name, phone_number) VALUES(?, ?)'
    c.execute(insert_statement, (name, phone_number))
    conn.commit()
    c.execute('SELECT * FROM guests ORDER BY guest_id DESC LIMIT 1')
    guest_phone_number = c.fetchone()[1]
    guest = Guest(guest_phone_number)
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
        guest.edit_phone_number(new_number)
    elif to_edit == 2:
        new_name = input("Please enter a new name >")
        guest.edit_name(new_name)


def create_hotel():
    tax_perc = float(input('Enter the hotel tax percentage (0.1 for 10%): '))
    name = input("Enter the name of the hotel: ")
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
    for index, hotel in enumerate(hotels):
        print(f'{index + 1}: {hotel[1]}')
    hotel_id = int(input('Which hotel do you want to manage? >'))
    hotel = Hotel(hotel_id)
    return hotel


def create_reservation():
    ''' Creates a new reservation

    Returns:
        reservation (obj): A reservation object.
    '''
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    phone_number = int(input('Enter guest\'s phone number >'))
    try:
        # If the guest doesn't already exist, move to the except statement.
        guest = get_guest(phone_number=phone_number)
    except TypeError:
        # Create a new guest from the phone_number already entered.
        guest = create_guest(phone_number=phone_number)
    guest_id = guest.guest_id
    num_rooms = int(
        int(input("Enter how many rooms the guest needs (no more than 5): ")))
    rooms = list()
    # Loop through each room the user wants and check if it is available.
    # If it is, add it to the rooms list, if not, ask again.
    for room in range(num_rooms):
        room_type = input(
            f"Enter the type of room #{room + 1} the guest wants (king, queen, double, single): ").casefold()
        c.execute(
            f'''SELECT * FROM rooms WHERE room_type_id = (SELECT room_type_id FROM room_types WHERE description = '{room_type}') AND availability = 1;''')
        rooms_available = c.fetchall()
        if len(rooms_available) < 1:
            room_type = input(
                f"Sorry that room type isn't avialable. Please try again. \nEnter the type of room #{room + 1} the guest wants (king, queen, double, single): ").casefold()
        rooms.append(rooms_available[0])

    # Get the user's check_in date, change to a datetime
    check_in = input('Enter your check in date (Jun 10 2020): ')
    check_in = datetime.datetime.strptime(check_in, '%b %d %Y')
    check_in = check_in.replace(hour=13, minute=00)
    # Get the number of days stating and create the check_out datetime from that
    days_staying = int(input("Enter how many days the guest be staying: "))
    check_out = (check_in + datetime.timedelta(days=days_staying))
    check_out = check_out.replace(hour=11, minute=00)

    # Add the reservation to the db
    insert_statement = 'INSERT INTO reservations (guest_id, check_in, check_out) VALUES (?, ?, ?)'
    c.execute(insert_statement, (guest_id, check_in, check_out))
    conn.commit()
    # Get the reservation back from the db
    c.execute('SELECT * FROM reservations ORDER BY reservation_id DESC LIMIT 1')
    reservation_id = c.fetchone()[0]
    reservation = Reservation(reservation_id)
    # Loop through each room the user wants and add it to the reservation_has_rooms table in the db.
    for room in rooms:
        res_to_rooms_insert = 'INSERT INTO reservation_has_rooms VALUES (?, ?)'
        c.execute(res_to_rooms_insert, (reservation.reservation_id, room[0]))
    conn.commit()

    return reservation


def get_reservation():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()

    phone_number = int(input('Enter guest\'s phone number >'))
    while True:
        try:
            # If the guest doesn't already exist, move to the except statement.
            guest = get_guest(phone_number=phone_number)
        except ValueError:
            print('No reservation under that phone number were found.')
            continue
        else:
            break
    query = 'SELECT * FROM reservations WHERE guest_id = (SELECT guest_id FROM guests WHERE phone_number = ?);'
    c.execute(query, (phone_number,))
    # Print the reservations for the specific guests and have them select which reservation by id.
    reservations = c.fetchall()
    for index, reservation in enumerate(reservations):
        print(
            f'{index + 1}: Check In: {reservation[2]} Check Out {reservation[3]}')
    reservation_id = int(input('Which reservation do you want to manage? >'))
    reservation = Reservation(reservation_id)
    return reservation_id


def main():
    # create_db_tables()
    # create_room_types()
    # create_rooms()
    print('Welcome to the Hotel Management System.')
    hotel_thing = input(
        'Which are you doing? \n1. Managing an Existing Hotel, or \n2. Creating a New Hotel? \n>')
    if int(hotel_thing) == 1:
        hotel = get_hotel()
    elif int(hotel_thing) == 2:
        hotel = create_hotel()
    else:
        return
    print(f'We are managing the {hotel.name} hotel.')
    while True:
        thing = input(
            'What do you want to do? \n1. Manage Guest \n2. Manage Reservation \n3. OTHER (TBD) \n>')
        if int(thing) == 1:
            guest_thing = input(
                'What do you want to do? \n1. Create Guest, \n2. Retrieve Guest \n3. Edit Guest Information \n>')
            if int(guest_thing) == 1:
                create_guest()
            elif int(guest_thing) == 2:
                get_guest()
            elif int(guest_thing) == 3:
                edit_guest()
            else:
                break
        elif int(thing) == 2:
            reservation_thing = input(
                'What do you want to do? \n1. New Reservation, \n2. View Reservation, \n3. Alter An Existing Reservation, \n4. Cancel Reservation\n>')
            if int(reservation_thing) == 1:
                create_reservation()
            elif int(reservation_thing) == 2:
                reservation = get_reservation()
                print(reservation)
            elif int(reservation_thing) == 3:
                alter_reservation()
            elif int(reservation_thing) == 4:
                cancel_reservation
        elif int(thing) == 3:
            pass
        else:
            break


if __name__ == "__main__":
    main()
