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
from create_db import create_db_tables


def create_guest():
    name = input("Enter the guest's name: ").capitalize()
    phone_number = input("Enter the guest's phone_number: ")

    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    insert_statement = 'INSERT INTO guests(name, phone_number) VALUES(?, ?)'
    c.execute(insert_statement, (name, phone_number))
    conn.commit()


def get_guest():
    phone_number = int(input('Enter guest\'s phone number > '))
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
        print(f'{index + 1}:{hotel[1]}')
    hotel_id = int(input('Which hotel do you want to manage? >'))
    hotel = Hotel(hotel_id)
    return hotel


def create_reservation():
    guest = get_guest()
    num_rooms = int(
        int(input("Enter how many rooms the guest needs (no more than 5): ")))
    room_types = list()
    for room in range(num_rooms):
        room_type = input(
            f"Enter the type of room #{room + 1} the guest wants (king, queen, double, single): ").casefold()
        room_types.append(room_type)

    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    for room in room_types:
        c.execute(
            'SELECT * FROM rooms WHERE room_type_id IN (SELECT room_type_id FROM room_types WHERE description = ? )', room)

    check_in = input('Enter your check in date (Jun 10 2020): ')
    check_in = datetime.datetime.strptime(check_in, '%b %d %Y')
    check_in = check_in.replace(hour=13, minute=00)
    days_staying = int(input("Enter how many days the guest be staying: "))

    check_out = (check_in + datetime.timedelta(days=days_staying))
    check_out = check_out.replace(hour=11, minute=00)


def main():
    # create_db_tables()
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
                'What do you want to do? \n 1. New Reservation, 2. Alter An Existing Reservation, Cancel Reservation')
            if int(reservation_thing) == 1:
                create_reservation()
            elif int(reservation_thing) == 2:
                alter_reservation()
            elif int(reservation_thing) == 3:
                cancel_reservation()
        elif int(thing) == 3:
            pass
        else:
            break


if __name__ == "__main__":
    main()
