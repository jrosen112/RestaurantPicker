import address


class Restaurant:
    CUISINE_TYPES = {
        "Mexican",
        "Tex-Mex",
        "Spanish",
        "American",
        "Diner",
        "Sushi",
        "Chinese",
        "Asian Fusion",
        "Hibachi",
        "Fast Food",
        "Cafe",
        "Burgers",
        "Steakhouse",
        "Italian",
        "Sandwiches"
    }

    def __init__(self, name: str,
                 website: str,
                 phone_num: str,
                 cuisine: str,
                 lat: float,
                 long: float,
                 addr: address.Address):
        if cuisine not in self.CUISINE_TYPES:
            raise ValueError("Specified cuisine type must be in the CUISINE_TYPES list.")
        self.cuisine = cuisine
        self.long = long
        self.lat = lat
        self.phone_num = phone_num
        self.website = website
        self.name = name
        self.addr = addr

    def __str__(self):
        for attr in vars(self):
            if attr == 'addr':
                print(self.addr)
                continue
            print(f'{attr}: {vars(self)[attr]}')
        return ""

    def create_tuple(self):
        helper = []
        for attr in reversed(vars(self)):
            print(attr, vars(self)[attr])
            if attr == 'addr':
                # helper.append(self.addr.street_addr)
                # helper.append(self.addr.apt_num)
                # helper.append(self.addr.city)
                # helper.append(self.addr.state)
                # helper.append(self.addr.zipcode)
                continue
            helper.append(vars(self)[attr])
        return tuple(helper)


# home = address.Address(street_addr="55 Edgewood Drive",
#                        apt_num="Unit 5B",
#                        city="Florham Park",
#                        state="New Jersey",
#                        zipcode="07932")
# titos = Restaurant(name="Tito's Burritos",
#                    website="https://www.apple.com",
#                    phone_num="9733090694",
#                    lat=25.0,
#                    long=-28.7,
#                    cuisine="Tex-Mex",
#                    addr=home)
# print(titos)
# print(titos.create_tuple())
