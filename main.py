import random
import ru_local
import hotel


# Creating an instance of the hotel class.
htl = hotel.Hotel()

# Reading from a file of available rooms.
with open('fund.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        r_num, type, capacity, comfort = line.split()

        htl.rooms.append(hotel.Room(type, int(capacity), comfort))
    htl.count_every_category()

# Reading from the guest reservation file.
with open('booking.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        booking_date, surname, name, patronymic, quantity, arrival_date, nights, budget = line.split()

        htl.orders.append(hotel.Order(hotel.Date(booking_date),
                                      surname,
                                      name,
                                      patronymic,
                                      int(quantity),
                                      hotel.Date(arrival_date),
                                      int(nights),
                                      int(budget)))

# We go through every day of the month.
for day in range(1, 31):
    print(f'\n{day}.03.2020')
    day_profit = 0
    day_lost_profit = 0

    # We evict those who need to be evicted.
    htl.departation_from_all_rooms(day)

    # Let's see who needs to be settled today.
    orders = htl.daily_check_orders(day)

    for order in orders:
        # We are looking for a suitable room according to your preferences.
        suitable_room = htl.find_suitable_room(order, discount=False)
        if suitable_room == (None, 0):
            suitable_room = htl.find_suitable_room(order, discount=True)
        profit = suitable_room[1]
        suitable_room = suitable_room[0]

        if suitable_room is not None:
            # There is a 25% chance that the guest can cancel the room. We take this into account here.
            rand_refuse = random.randint(1, 4)

            if rand_refuse == 4:
                print(f'{order.surname} {order.name} {order.patronymic} {ru_local.DECLINE}')
                day_lost_profit += order.budget * order.quantity

            else:
                print(f'{ru_local.SETTLED} {order.surname} {order.name} '
                      f'{order.patronymic} {ru_local.AMOUNT} {order.quantity}')
                day_profit += profit
                suitable_room.booking.append(order)

        # If the room is not found, then we consider the lost income.
        else:
            print(f'{ru_local.NOT_SUITABLE} {order.surname} {order.name} '
                  f'{order.patronymic} {ru_local.AMOUNT} {order.quantity}')
            day_lost_profit += order.budget * order.quantity

    # We check the occupancy of the rooms.
    general_available = htl.check_general_available(day)

    # We display statistics for the day.
    print(f'\n{ru_local.BUSY_ROOMS} {general_available["non_available"]}')
    print(f'{ru_local.FREE_ROOMS} {general_available["available"]}')

    print(ru_local.PERCENT_EACH)
    for category, value in htl.check_general_category_load(day).items():
        print(f'{category}: {value}%')
    print(f'{ru_local.PERCENT_ALL} {general_available["non_available"] / len(htl.rooms) * 100}%')

    print(f'{ru_local.REVENUE} {day_profit}')
    print(f'{ru_local.LOSSES} {day_lost_profit}')
