-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE month =7 AND day = 28 AND street =
'Humphrey Street';

--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery



SELECT * FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10;



--+-----+------+-------+-----+------+--------+----------+---------------+
| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 258 | 2021 | 7     | 28  | 10   | 8      | entrance | R3G7486       |
| 259 | 2021 | 7     | 28  | 10   | 14     | entrance | 13FNH73       |
| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
| 268 | 2021 | 7     | 28  | 10   | 35     | exit     | 1106N58       |
| 269 | 2021 | 7     | 28  | 10   | 42     | entrance | NRYN856       |
| 270 | 2021 | 7     | 28  | 10   | 44     | entrance | WD5M8I6       |
| 271 | 2021 | 7     | 28  | 10   | 55     | entrance | V47T75I       |

SELECT * FROM people WHERE liscence_plate = '13FNH73';

+--------+--------+----------------+-----------------+---------------+
|   id   |  name  |  phone_number  | passport_number | license_plate |
+--------+--------+----------------+-----------------+---------------+
| 745650 | Sophia | (027) 555-1068 | 3642612721      | 13FNH73       |
+--------+--------+----------------+-----------------+---------------+



SELECT * FROM passengers WHERE passport_number = 3642612721;


+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 6         | 3642612721      | 8A   |
| 31        | 3642612721      | 9B   |
| 43        | 3642612721      | 2C   |
+-----------+-----------------+------+


SELECT * FROM flights WHERE id = (SELECT flight_id FROM passengers WHERE passport_number = 3642612721) AND day = 28 AND month = 7;

+----+-------------------+------------------------+------+-------+-----+------+--------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+----+-------------------+------------------------+------+-------+-----+------+--------+
| 6  | 8                 | 5                      | 2021 | 7     | 28  | 13   | 49     |
+----+-------------------+------------------------+------+-------+-----+------+--------+



SELECT * FROM airports WHERE id in (SELECT destination_airport_id FROM flights WHERE id in (SELECT flight_id FROM passengers WHERE passport_number = 3642612721) AND day = 28 AND month = 7);


+----+--------------+-----------------------------------------+--------+
| id | abbreviation |                full_name                |  city  |
+----+--------------+-----------------------------------------+--------+
| 5  | DFS          | Dallas/Fort Worth International Airport | Dallas |
+----+--------------+-----------------------------------------+--------+.


SELECT * FROM passengers where flight_id = 6;
+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 6         | 3835860232      | 9A   |
| 6         | 1618186613      | 2C   |
| 6         | 7179245843      | 3B   |
| 6         | 1682575122      | 4B   |
| 6         | 7597790505      | 5D   |
| 6         | 6128131458      | 6B   |
| 6         | 6264773605      | 7D   |
| 6         | 3642612721      | 8A   |
+-----------+-----------------+------+



SELECT passport_number FROM passengers where flight_id = 6 AND seat = '9A';


SELECT * FROM people where passport_number = (SELECT passport_number FROM passengers where flight_id = 6 AND seat = '9A');

+--------+--------+----------------+-----------------+---------------+
|   id   |  name  |  phone_number  | passport_number | license_plate |
+--------+--------+----------------+-----------------+---------------+
| 780088 | Nicole | (123) 555-5144 | 3835860232      | 91S1K32       |
+--------+--------+----------------+-----------------+---------------+


SELECT * FROM phone_calls WHERE caller =  (SELECT phone_number FROM people WHERE license_plate = '13FNH73') AND receiver =(SELECT phone_number FROM people where passport_number = (SELECT passport_number FROM passengers where flight_id = 6 AND seat = '9A'));



| 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.' |



SELECT * FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location like 'Leggett Street';

SELECT name FROM people JOIN bank_accounts on people.id = bank_accounts.person_id WHERE account_number in ( SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location like 'Leggett Street');

+---------+
|  name   |
+---------+
| Bruce   |
| Kaelyn  |
| Diana   |
| Brooke  |
| Kenny   |
| Iman    |
| Luca    |
| Taylor  |
| Benista |
+---------+


SELECT * FROM passengers
WHERE passport_number in
(SELECT passport_number FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE account_number in
(SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street')
AND license_plate in
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute >= 35 ))
AND flight_id IN
(SELECT id FROM flights
WHERE month = 7 AND day = 29 AND origin_airport_id =
(SELECT id FROM airports
WHERE full_name like 'fiftyville%') ORDER BY hour, minute LIMIT 1 );


+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 36        | 1988161715      | 6D   |
+-----------+-----------------+------+

SELECT * FROM people where passport_number =
(SELECT passport_number FROM passengers
WHERE passport_number in
(SELECT passport_number FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE account_number in
(SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street')
AND license_plate in
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10))
AND flight_id IN
(SELECT id FROM flights
WHERE month = 7 AND day = 29 AND origin_airport_id =
(SELECT id FROM airports
WHERE full_name like 'fiftyville%') ORDER BY hour, minute LIMIT 1 ));


+--------+
|  name  |
+--------+
| Taylor |


SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM  flights
WHERE id = (SELECT flight_id FROM passengers
WHERE passport_number in
(SELECT passport_number FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE account_number in
(SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street')
AND license_plate in
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 ))
AND flight_id IN
(SELECT id FROM flights
WHERE month = 7 AND day = 29 AND origin_airport_id =
(SELECT id FROM airports
WHERE full_name like 'fiftyville%') ORDER BY hour, minute LIMIT 1 )));


+---------------+
|     city      |
+---------------+
| New York City |
+---------------




SELECT receiver FROM phone_calls where caller = (SELECT phone_number FROM people where passport_number =
(SELECT passport_number FROM passengers
WHERE passport_number in
(SELECT passport_number FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE account_number in
(SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street')
AND license_plate in
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 ))
AND flight_id IN
(SELECT id FROM flights
WHERE month = 7 AND day = 29 AND origin_airport_id =
(SELECT id FROM airports
WHERE full_name like 'fiftyville%') ORDER BY hour, minute LIMIT 1 )))
AND duration < 60
AND month = 7
AND day = 28;



SELECT * FROM people WHERE phone_number = (SELECT receiver FROM phone_calls where caller = (SELECT phone_number FROM people where passport_number =
(SELECT passport_number FROM passengers
WHERE passport_number in
(SELECT passport_number FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE account_number in
(SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street')
AND license_plate in
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 ))
AND flight_id IN
(SELECT id FROM flights
WHERE month = 7 AND day = 29 AND origin_airport_id =
(SELECT id FROM airports
WHERE full_name like 'fiftyville%') ORDER BY hour, minute LIMIT 1 )))
AND duration < 60
AND month = 7
AND day = 28);


+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 250277 | James | (676) 555-6554 | 2438825627      | Q13SVG6       |
+--------+-------+----------------+-----------------+---------------+