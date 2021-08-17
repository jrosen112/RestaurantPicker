import sqlite3
from sqlite3 import Error
import restaurants
import address
import csv


def create_connection(db_file: str) -> None:
    """ creates connection to sqlite3 database """
    conn = None
    try:
        conn = sqlite3.connect(database=db_file)
        print(f'SQLite version: {sqlite3.version}')
    except Error as e:
        print(f'Connection error: {e}')
    finally:
        if conn:
            conn.close()


def create_restaurant_table(conn: sqlite3.Connection,
                            sql_query: str) -> None:
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS restaurants")
        cursor.execute(sql_query)
    except Error as e:
        print(f'Create table error: {e}')


def create_address_table(conn: sqlite3.Connection,
                         sql_query: str) -> None:
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS addresses")
        cursor.execute(sql_query)
    except Error as e:
        print(f'Create table error: {e}')


def create_address(conn: sqlite3.Connection, addr: tuple) -> int:
    cursor = conn.cursor()
    if len(addr) == 5:
        query = """
                INSERT INTO addresses(street_addr, apt_num, city, state, zipcode)
                VALUES (?,?,?,?,?)
        """
        cursor.execute(query, addr)
    else:
        query = """
                INSERT INTO addresses(street_addr, city, state, zipcode)
                VALUES (?,?,?,?)
        """
        cursor.execute(query, addr)
    conn.commit()
    return cursor.lastrowid


def create_restaurant(conn: sqlite3.Connection, rest: tuple) -> int:
    cursor = conn.cursor()
    query = """
        INSERT INTO restaurants(name, website, phone_num, latitude, longitude, cuisine)
        VALUES (?,?,?,?,?,?)
    """
    cursor.execute(query, rest)
    conn.commit()
    return cursor.lastrowid


def consume_csv(path: str, conn=None) -> str:
    num_rows = 0
    with open(file=path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            print(row[0])
            print(', '.join(row))
            num_rows += 1
    return f'Number of rows added to DB: {num_rows}'


def main():
    rest_table = """
        CREATE TABLE IF NOT EXISTS restaurants (
            id integer PRIMARY KEY,
            name text NOT NULL,
            website text,
            phone_num text,
            cuisine text,
            latitude decimal(8, 6),
            longitude decimal(9, 6),
            address_id integer,
            FOREIGN KEY (address_id) REFERENCES addresses (id)
        );
    """
    addr_table = """
        CREATE TABLE addresses (
            id integer PRIMARY KEY,
            street_addr text NOT NULL,
            apt_num text,
            city text NOT NULL,
            state text NOT NULL,
            zipcode text NOT NULL
        );
    """
    db_file = r'./sqlite/db/testDB.db'
    titos_addr = address.Address(street_addr="356 Springfield Avenue",
                                 city="Summit",
                                 state="New Jersey",
                                 zipcode="07901")
    titos = restaurants.Restaurant(name="Tito's Burritos",
                                   cuisine="Tex-Mex",
                                   website="https://www.titosburritos.com",
                                   phone_num="9082773710",
                                   lat=40.71820,
                                   long=-74.35688,
                                   addr=titos_addr)
    rest_tuple = titos.create_tuple()
    titos_tuple = titos_addr.create_tuple()
    conn = sqlite3.connect(db_file)
    if conn is not None:
        create_address_table(conn, addr_table)
        create_restaurant_table(conn, rest_table)
    else:
        print("Error creating tables.")
    with conn:
        print(create_address(conn, titos_tuple))
        print(create_restaurant(conn, rest_tuple))
    conn.close()
    consume_csv(r'/Users/jaredrosen/Desktop/restaurants.csv')


if __name__ == "__main__":
    main()
