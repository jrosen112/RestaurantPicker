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
        print("Creating table 'restaurants'...")
    except Error as e:
        print(f'Failed to create \'restaurants\' table: {e}')
    print("'restaurants' table created successfully.\n")


def create_address_table(conn: sqlite3.Connection,
                         sql_query: str) -> None:
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS addresses")
        cursor.execute(sql_query)
        print("Creating table 'addresses'...")
    except Error as e:
        print(f'Failed to create \'addresses\' table: {e}')
    print("'addresses' table created successfully.\n")


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


def consume_csv(filetype: str, path: str, conn: sqlite3.Connection) -> None:
    num_rows = 0
    types = ["address", "restaurant"]
    if filetype not in types:
        print("CSV file must contain information on either Restaurants or Addresses.")
        return
    if filetype == types[1]:
        with open(file=path, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            print(f'Adding rows from {path} to database...')
            for row in reader:
                if num_rows == 0:  # hacky way to skip headers line and move to actual data
                    num_rows += 1
                    continue
                name = row[0]
                website = row[1]
                phone = row[2]
                lat = row[3]
                longitude = row[4]
                cuisine = row[5]
                new_restaurant = restaurants.Restaurant(name=name,
                                                        website=website,
                                                        phone_num=phone,
                                                        lat=float(lat),
                                                        long=float(longitude),
                                                        cuisine=cuisine)
                r_tuple = new_restaurant.create_tuple()
                create_restaurant(conn, r_tuple)
                num_rows += 1
                print(f'Added row for {name}.')
    if filetype == types[2]:
        with open(file=path, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            print(f'Adding rows from {path} to database...')
            for row in reader:
                if num_rows == 0:
                    num_rows += 1
                    continue
                if len(row) == 5:
                    street_addr = row[0]
                    apt_num = row[1]
                    city = row[2]
                    state = row[3]
                    zipcode = row[4]
                    new_addr = address.Address(street_addr=street_addr,
                                               apt_num=apt_num,
                                               city=city,
                                               state=state,
                                               zipcode=zipcode)
                    addr_tuple = new_addr.create_tuple()
                    create_address(conn, addr_tuple)
                else:
                    street_addr = row[0]
                    city = row[1]
                    state = row[2]
                    zipcode = row[3]
                    new_addr = address.Address(street_addr=street_addr,
                                               city=city,
                                               state=state,
                                               zipcode=zipcode)
                    addr_tuple = new_addr.create_tuple()
                    create_address(conn, addr_tuple)
                num_rows += 1
                print(f'Added new address.')
    print(f'\nSuccessfully parsed {path}.\nNumber of rows added to the database: {num_rows-1}\n')


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
    print(f'Opening connection to the database \'{db_file}\'...\n')
    if conn is not None:
        create_address_table(conn, addr_table)
        create_restaurant_table(conn, rest_table)
        create_address(conn, titos_tuple)
        create_restaurant(conn, rest_tuple)
    else:
        print("There was an error making a connection to the database.")
    consume_csv(filetype="restaurant", path=r'/Users/jaredrosen/Desktop/restaurants.csv', conn=conn)
    conn.close()
    print("Database connection closed.")


if __name__ == "__main__":
    main()
