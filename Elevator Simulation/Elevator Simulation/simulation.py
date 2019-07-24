import os
import time

from passenger import Passenger
from elevators import ElevatorFactory
from building import Building



class SimulationEngine():
    """
    Class responsible for running the simulation by working with the Building,
    Passengers, and Elevator classes

    Attributes:
        num_floors: number of floors in the building indexed from 0 to num_floors-1
        passenger_list: list of passengers
        elevator: elevator class used in the building
        building: building class
    """

    END_MESSAGE = "All passengers have been served - End of simulation"
    TIME_MESSAGE = "Average journey time: %s"
    MOVE_MESSAGE = "Elevator moved from floor %s to floor %s"
    PICKUP_MESSAGE = "Elevator picks up passenger %s at floor %s"
    DROPOFF_MESSAGE = "Elevator drops off passenger %s at floor %s"

    COLUMN_NAMES = ["Elevator", "|", "Floor", "# people"]
    FLOOR_FORMAT = "{:>10}" * len(COLUMN_NAMES)
    ELEVATOR_ON_FLOOR = "X"
    NO_ELEVATOR = " "
    DELIMITER = "|"

    TIME_PER_FLOOR = 1.5
    STOP_TIME = 6

    def __init__(self, num_floors, total_passengers, elevator_type, capacity, should_plot=True):
        self.num_floors = num_floors
        self.total_passengers = total_passengers
        self.elevator_type = elevator_type
        self.elevator_capacity = capacity
        self.should_plot = should_plot

        # Initialize passengers, elevator, and Building
        self.reset()

    def reset(self):
        """
        Initializes/resets the simulation to its initial state
        """
        # Generate a list of passengers based on total number of passengers
        self.passenger_list = [Passenger(i, self.num_floors)
                               for i in range(1, self.total_passengers + 1)]

        self.elevator = ElevatorFactory.get_elevator(self.num_floors,
                                                     self.elevator_type, self.passenger_list, self.elevator_capacity)

        self.building = Building(self.num_floors, self.passenger_list)

    def run(self):
        """
        Main method for simulation. The while True loop continues until
        all requests are fulfilled
        """
        self._print_state([], 0, True)
        total_wait_time = 0
        distance_moved = 0

        while True:
            # Used to print current state
            passenger_movements = []

            # Pick-up/drop-off passengers on current floor
            for passenger in self.elevator.requests:
                if passenger.at_destination:
                    continue

                # Add time waited to total
                total_wait_time += distance_moved * self.TIME_PER_FLOOR + self.STOP_TIME

                # Try pick-up
                pickup_move = self._pickup_passenger(passenger)
                # If passenger entered the elevator, store movement
                if pickup_move is not None:
                    passenger_movements.append(pickup_move)

                # Try drop-off
                dropoff_move = self._dropoff_passenger(passenger)
                # If passenger left the elevator, store movement
                if dropoff_move is not None:
                    passenger_movements.append(dropoff_move)

            # If there is no request left, we end the simulation and break the loop.
            if self.elevator.all_requests_completed():
                average_journey = 0
                if self.total_passengers != 0:
                    average_journey = total_wait_time / self.total_passengers

                if self.should_plot:
                    print(self.END_MESSAGE)
                    print(self.TIME_MESSAGE % (average_journey))

                return average_journey

            distance_moved = self.elevator.move()
            self._print_state(passenger_movements, distance_moved)

    def _pickup_passenger(self, passenger):
        """
        Pick-up passenger given that elevator is on the floor
        and the maximum capacity is not reached
        """
        if passenger.current == self.elevator.curr_floor \
                and passenger.in_elevator == False \
                and self.elevator.num_passengers < self.elevator.capacity:
            passenger.in_elevator = True
            self.elevator.num_passengers += 1

            return (self.PICKUP_MESSAGE %
                    (passenger.id, self.elevator.curr_floor))

        return None

    def _dropoff_passenger(self, passenger):
        """
        Drop-off passenger given that the destination is reached
        """
        if passenger.destination == self.elevator.curr_floor \
                and passenger.in_elevator == True:
            self.elevator.num_passengers -= 1
            passenger.at_destination = True

            return (self.DROPOFF_MESSAGE %
                    (passenger.id, self.elevator.curr_floor))

        return None

    def _print_state(self, passenger_movements, distance_moved, initial=False):
        """
        Prints the current state of the simulation
        """
        if not self.should_plot:
            return

        # Clear output
        os.system('clear')
        # clear_output(wait=True)

        # Illustration of current state
        print(self.FLOOR_FORMAT.format(*self.COLUMN_NAMES))

        for floor in range(self.num_floors - 1, -1, -1):
            floor_elements = []

            if floor == self.elevator.curr_floor:
                floor_elements.append(self.ELEVATOR_ON_FLOOR)
            else:
                floor_elements.append(self.NO_ELEVATOR)

            floor_elements.append(self.DELIMITER)
            floor_elements.append(floor)
            floor_elements.append(str(self.building.get_passengers_on_floor(floor)))

            print(self.FLOOR_FORMAT.format(*floor_elements))

        if initial:
            time.sleep(1)
            return

        print("=" * 50)
        print("Number of people in elevator while moving: %s" % self.elevator.num_passengers)
        print("Number of passengers who have received service: %s out of %s"
              % (self.elevator.requests_served(), len(self.elevator.requests)))

        # Display next elevator movement
        if self.elevator.is_moving_up():
            print(self.MOVE_MESSAGE %
                  (self.elevator.curr_floor - distance_moved, self.elevator.curr_floor))
        elif not self.elevator.is_moving_up():
            print(self.MOVE_MESSAGE
                  % (self.elevator.curr_floor + distance_moved, self.elevator.curr_floor))

        # Display passenger movements
        print("=" * 50)
        for movement in passenger_movements:
            print(movement)

        time.sleep(1)