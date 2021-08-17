import re


class Address:
    STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
              "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
              "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
              "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
              "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
              "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
              "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Washington, D.C.",
              "West Virginia", "Wisconsin", "Wyoming"]

    def __init__(self, street_addr: str,
                 city: str,
                 state: str,
                 zipcode: str,
                 apt_num: str = None):
        self.zipcode = self.zip_regex(zipcode)
        if state not in self.STATES:
            raise ValueError("Please enter a valid U.S. state.")
        self.state = state
        self.city = city
        self.apt_num = apt_num
        self.street_addr = street_addr

    def __str__(self):
        print(f'Street address: {self.street_addr}')
        if self.apt_num:
            print(f'Apartment: {self.apt_num}')
        print(f'City, state: {self.city}, {self.state}')
        print(f'Zip code: {self.zipcode}')
        return ""

    @staticmethod
    def zip_regex(zipcode: str) -> str:
        postal_code = re.search(pattern=r'.*(\d{5}(\-\d{4})?)$', string=zipcode)
        if postal_code is not None:
            return postal_code.group(0)
        else:
            raise ValueError("Enter a valid U.S. zipcode.")

    def create_tuple(self):
        helper = []
        for attr in reversed(vars(self)):
            helper.append(vars(self)[attr])
        return tuple(helper)


# home = Address(street_addr="55 Edgewood Drive",
#                apt_num="Unit 5B",
#                city="Florham Park",
#                state="New Jersey",
#                zipcode="07932")
# print(home)
# print(home.create_tuple())
