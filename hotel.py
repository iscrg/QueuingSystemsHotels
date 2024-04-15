import ru_local


class Date:
    """
    The class is used as a data type for convenient date storage.
    """

    def __init__(self,
                 date: str = None,
                 day: int = None,
                 month: int = None,
                 year: int = None) -> None:
        """
        Initialise date using either the full date or divided by variables.

        :param date: Date in format DD.MM.YYYY
        :param day: Day
        :param month: Month
        :param year: Year

        :return: None
        """
        if date is not None:
            day, month, year = map(int, date.split('.'))

        self.day = day
        self.month = month
        self.year = year


class Order:
    """
    The class is a customer's order that has
    the necessary parameters specified below.
    """

    def __init__(self,
                 booking_date: Date,
                 surname: str,
                 name: str,
                 patronymic: str,
                 quantity: int,
                 arrival_date: Date,
                 nights: int,
                 budget: int) -> None:
        """
        Initializes the order. Counts the departure date.

        :param booking_date: Date, when customer booked room.
        :param surname: Surname
        :param name: Name
        :param patronymic: Patronymic
        :param quantity: The quantity of people who need to be settled.
        :param arrival_date: Check-in date
        :param nights: The number of desired nights in the room.
        :param budget: The desired budget.

        :return: None
        """
        self.booking_date = booking_date
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.quantity = quantity
        self.arrival_date = arrival_date
        self.nights = nights
        self.budget = budget
        self.departure_date = Date(day=self.arrival_date.day + self.nights,
                                   month=self.arrival_date.month,
                                   year=self.arrival_date.year)


class Room:
    """
    The Room class represents a room in a hotel.
    """

    def __init__(self,
                 type: str,
                 capacity: int,
                 comfort: str,
                 booking: Order = None) -> None:
        """
        Initialises the room. Calculates price of the room.

        :param type: Type of the room.
        :param capacity: Amount of people who can live in the room.
        :param comfort: Comfort of the room.
        :param booking: Booking of the room.
        :return: None
        """
        self.type = type
        self.capacity = capacity
        self.comfort = comfort
        self.booking = [booking] if booking is not None else []
        self.price = Hotel.type_conf[type] * Hotel.comfort_conf[comfort]

    def check_departure(self, day: int) -> bool:
        """
        Checks if the person needs to leave the room.

        :param day: Date to check.
        :return: None
        """
        if self.booking != [] and day == self.booking[0].departure_date.day:
            return True

    def departure(self) -> None:
        """
        Departure guest from room.
        :return: None
        """
        self.booking.pop(0)


class Hotel:
    """
    The Hotel class represents a hotel.
    """
    num_categories = {
        ru_local.SINGLE_ROOM: 0,
        ru_local.DOUBLE_ROOM: 0,
        ru_local.HALF_LUXURY_ROOM: 0,
        ru_local.LUXURY_ROOM: 0,
        ru_local.STANDART: 0,
        ru_local.IMPROVED_STANDART: 0,
        ru_local.APARTMENT: 0
    }

    type_conf = {
        ru_local.SINGLE_ROOM: 2900,
        ru_local.DOUBLE_ROOM: 2300,
        ru_local.HALF_LUXURY_ROOM: 3200,
        ru_local.LUXURY_ROOM: 4100
    }

    comfort_conf = {
        ru_local.STANDART: 1.0,
        ru_local.IMPROVED_STANDART: 1.2,
        ru_local.APARTMENT: 1.5
    }

    meal_price = {
        ru_local.WITHOUT: 0,
        ru_local.BREAKFAST: 280,
        ru_local.HALF_BOARD: 1000
    }

    def __init__(self):
        self.rooms = []
        self.orders = []

    def departation_from_all_rooms(self, day: int) -> None:
        """
        The method evicts the guests from the rooms according to the day of the eviction.
        :param day: The set day according to which people need to be evicted.
        :return: None
        """
        for room in self.rooms:
            if room.check_departure(day):
                print(f'{room.booking[0].surname} {room.booking[0].name} '
                      f'{room.booking[0].patronymic} {ru_local.LEAVE}')
                room.departure()

    def check_general_available(self, day: int) -> dict:
        """
        Checks statistics of rooms availability.

        :param day: Date to check.
        :return: Dicitonary of the rooms that are available or no available.
        """
        available = 0
        for room in self.rooms:

            if (room.booking == []) or (room.booking[0].arrival_date.day > day):
                available += 1

        non_available = len(self.rooms) - available

        return {'available': available, 'non_available': non_available}

    def count_every_category(self) -> None:
        """
        Counts the number of rooms in each category.

        :return: None
        """
        for room in self.rooms:
            Hotel.num_categories[room.type] += 1
            Hotel.num_categories[room.comfort] += 1

    def check_general_category_load(self, day: int) -> dict:
        """
        Percentage of occupancy of individual room categories.

        :param day: Date to check.
        :return: Dictionary with percentage of occupancy of individual room categories.
        """

        category_non_available = {
            ru_local.SINGLE_ROOM: 0,
            ru_local.DOUBLE_ROOM: 0,
            ru_local.HALF_LUXURY_ROOM: 0,
            ru_local.LUXURY_ROOM: 0,
            ru_local.STANDART: 0,
            ru_local.IMPROVED_STANDART: 0,
            ru_local.APARTMENT: 0
        }

        for room in self.rooms:
            if (room.booking != []) and (room.booking[0].arrival_date.day <= day):
                category_non_available[room.type] += 1
                category_non_available[room.comfort] += 1

        res = {}
        for category in category_non_available:
            res[category] = (category_non_available[category] / Hotel.num_categories[category]) * 100
        return res

    def daily_check_orders(self, day: int) -> list:
        """
        Checks the orders that need to be processed on the specified day.

        :param day: Date to check.
        :return: Suitable orders.
        """
        suitable_orders = []
        for order in self.orders:
            if day == order.booking_date.day:
                suitable_orders.append(order)
        return suitable_orders

    def find_suitable_room(self, order: Order, discount: bool) -> tuple:
        """
        The method is looking for a room in which you can populate this order with maximum benefit.
        :param order: Current order.
        :param discount: The availability of a discount as a result of the offer of rooms with
                         a larger capacity due to the lack of suitable ones.
        :return: (Maximum profitable room, Profit from maximum profitable room)
        """
        if discount:
            capacity_ratio = 1
            price_ratio = 0.7
        else:
            capacity_ratio = 0
            price_ratio = 1

        max_profit = 0
        max_profit_room = None
        profit_from_room = 0

        # We check all the rooms and choose the most suitable one.
        for room in self.rooms:
            # We check that the room is available on the specified date,
            # that it is suitable for capacity and budget.
            if ((room.booking == []) or (order.arrival_date.day >= room.booking[-1].departure_date.day)) and \
                    (order.quantity == room.capacity * capacity_ratio) and \
                    (order.budget >= room.price * price_ratio):

                # Selection of suitable food.
                if order.budget >= room.price + Hotel.meal_price[ru_local.HALF_BOARD]:
                    profit_from_room = (room.price + Hotel.meal_price[ru_local.HALF_BOARD]) * order.quantity

                    if max_profit < profit_from_room:
                        max_profit_room = room
                        max_profit = profit_from_room

                elif order.budget >= room.price + Hotel.meal_price[ru_local.BREAKFAST]:
                    profit_from_room = (room.price + Hotel.meal_price[
                        ru_local.BREAKFAST]) * order.quantity

                    if max_profit < profit_from_room:
                        max_profit_room = room
                        max_profit = profit_from_room

                else:
                    profit_from_room = room.price * order.quantity

                    # Checking that the room will bring maximum profit.
                    if max_profit < profit_from_room:
                        max_profit_room = room
                        max_profit = profit_from_room

        return max_profit_room, max_profit
