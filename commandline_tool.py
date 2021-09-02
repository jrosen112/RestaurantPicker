import db_scripts as scripts
import restaurants
import address


def main_loop() -> None:
    print(f'Okay, let\'s get started adding a restaurant and its address.')
    street_addr = input("What's the street address?\n").strip()
    apt_num = input("What's the apartment number? Or hit enter if there is none. ")
    city_state = input("Enter the city, state, and zipcode separated by commas.\n").split(", ")
    city = city_state[0]
    state = city_state[1]
    zipcode = city_state[2]
    print(f'City: {city}, State: {state}, Zip: {zipcode}')
    addr = address.Address(street_addr=street_addr,
                           city=city,
                           state=state,
                           apt_num=apt_num,
                           zipcode=zipcode)
    print(addr)
    addr_tuple = addr.create_tuple()


def main():
    main_loop()


if __name__ == '__main__':
    main()
