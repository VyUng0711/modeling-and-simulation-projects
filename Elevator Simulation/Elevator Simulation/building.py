class Building():
    """
    Class representing the Building entity in the simulation

    Attributes:
        num_floors: number of floors in the building indexed from 0 to num_floors-1
        passenger_list: list of passengers
    """
    def __init__(self, num_floors, passenger_list):
        self.num_floors = num_floors
        self.passenger_list = passenger_list

    def get_passengers_on_floor(self, floor):
        passenger_count = 0

        for passenger in self.passenger_list:
            if passenger.in_elevator == False and passenger.current == floor:
                passenger_count += 1

        return passenger_count