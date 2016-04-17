#!/usr/bin/python3.4

from TM import TM, Connector
from datetime import datetime

TO_FLY = """
INSERT INTO fly_booking
(client_name, fly_number, fly_from, fly_to, fly_date, money)
VALUES('%s', '%s', '%s', '%s', '%s', %s);
"""

TO_HOTEL = """
INSERT INTO hotel_booking
(client_name, hotel_name, arrival, departure)
VALUES('%s', '%s', '%s', '%s');
"""


def run():
    fly_conn = Connector(dbname='fly').get_connect()
    hotel_conn = Connector(dbname='hotel').get_connect()
    tm = TM()

    str_now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    fly_query = TO_FLY % ('client_1', 'fly_1', 'some_place_1', 'some_place_2', str_now, 10)
    hotel_query_fly = TO_HOTEL % ('client_1', 'hotel1', str_now, str_now)
    hotel_query_other = TO_HOTEL % ('client_2', 'hotel1', str_now, str_now)

    tm.add(fly_query, fly_conn)
    tm.add(hotel_query_fly, hotel_conn)
    tm.add(hotel_query_other, hotel_conn)

    tm.commit()

    fly_conn.close()
    hotel_conn.close()

if __name__ == '__main__':
    run()
