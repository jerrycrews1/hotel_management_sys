-- SQLite
-- SELECT * FROM rooms WHERE room_type_id = (SELECT room_type_id FROM room_types WHERE description = 'king') AND availability = 1;

SELECT * FROM reservations WHERE guest_id = (SELECT guest_id FROM guests WHERE phone_number = '2293550704');

-- -- select rooms with available dates --
-- SELECT room_num FROM rooms JOIN reservation_has_rooms ON(room_num = room_id) JOIN reservations USING(reservation_id) JOIN room_types USING(room_type_id);


-- Gets rooms that belong to a reservation and overlap. Use as subquery NOT IN
-- SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE MAX(check_in, '2021-08-11 15:00:00') > MIN(check_out, '2021-08-13 11:00:00')  ;


SELECT room_num FROM rooms WHERE room_num NOT IN (SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE MAX(check_in, '2021-08-11 15:00:00') < MIN(check_out, '2021-08-13 11:00:00')  ;)


SELECT room_num FROM rooms WHERE room_num NOT IN (SELECT room_id FROM reservation_has_rooms JOIN reservations USING(reservation_id) WHERE check_in <= '2021-08-11 13:00:00' OR '2021-08-11 13:00:00' < check_out OR '2021-08-11 13:00:00' <= check_in OR '2021-08-11 13:00:00' < check_out OR check_in <= '2021-08-13 11:00:00' OR '2021-08-13 11:00:00' < check_out OR '2021-08-11 13:00:00' <= check_out OR check_out < '2021-08-11 13:00:00')

check_in > '2021-08-11 13:00:00' AND '2021-08-11 13:00:00' >= check_out AND '2021-08-11 13:00:00' > check_in AND '2021-08-11 13:00:00' >= check_out AND check_in > '2021-08-13 11:00:00' AND '2021-08-13 11:00:00'>= check_out AND '2021-08-11 13:00:00' > check_out AND check_out >= '2021-08-11 13:00:00'