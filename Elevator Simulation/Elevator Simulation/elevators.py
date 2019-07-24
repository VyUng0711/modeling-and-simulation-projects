from enum import Enum


class ElevatorTypes(Enum):
    shabbat = 'shabbat'
    ordinary = 'ordinary'


class ElevatorFactory():
    """
    Factory that returns instances of different types of elevators
    """

    def get_elevator(num_floors, elevator_type, requests=[], capacity=5):
        if elevator_type == ElevatorTypes.shabbat:
            return ShabbatElevator(num_floors, requests, capacity)
        elif elevator_type == ElevatorTypes.ordinary:
            return OrdinaryElevator(num_floors, requests, capacity)
        else:
            return None

    get_elevator = staticmethod(get_elevator)


class AbstractElevator():
    """
    Class representing the Elevator entity in the simulation

    Attributes:
        num_floors: Number of floors in the building indexed from 0 to num_floors-1
        requests: List of requests from all the passengers, this is specified at once in the start by user
        capacity: Maximum number of passengers that the elevator could carry
        curr_floor: The floor that the elevator is currently on
        direction: Indicator whether the elevator is moving up or down
        num_passengers: number of passengers currently in the elevator
    """

    DEFAULT_NUM_PASSENGERS = 0
    STARTING_FLOOR = 0

    # Directions
    DIRECTION_UP = 0
    DIRECTION_DOWN = 1

    def __init__(self, num_floors, requests=[], capacity=5):
        self.num_floors = num_floors
        self.requests = requests
        self.capacity = capacity

        self.curr_floor = self.STARTING_FLOOR
        self.direction = self.DIRECTION_UP
        self.num_passengers = self.DEFAULT_NUM_PASSENGERS

    def move(self):
        raise NotImplementedError()

    def all_requests_completed(self):
        for request in self.requests:
            if not request.at_destination:
                return False

        return True

    def requests_served(self):
        return 1 + sum([request.at_destination
                        for request in self.requests])

    def is_moving_up(self):
        return self.direction == self.DIRECTION_UP


class ShabbatElevator(AbstractElevator):
    """
    Elavator that inherits from the Abstract elevator class
    and moves with the logic of a Shabbat elevator
    """

    def __init__(self, num_floors, requests=[], capacity=5):
        AbstractElevator.__init__(self, num_floors, requests, capacity)

    def move(self):
        """
        Moving logic for the elevator: moves by one floor, either up or down
        Switches direction when it reaches top/bottom floor

        Return: Number of floors travelled
        """

        # Change direction if on top/bottom floor
        if self.curr_floor == 0:
            self.direction = self.DIRECTION_UP
        elif self.curr_floor == self.num_floors - 1:
            self.direction = self.DIRECTION_DOWN

        # Move by 1 floor depending on direction
        if self.direction == self.DIRECTION_UP:
            self.curr_floor += 1
        elif self.direction == self.DIRECTION_DOWN:
            self.curr_floor -= 1

        return 1


class OrdinaryElevator(AbstractElevator):
    """
    Elavator that inherits from the Abstract elevator class
    and moves like an ordinary elevator
    """

    def __init__(self, num_floors, requests=[], capacity=5):
        AbstractElevator.__init__(self, num_floors, requests, capacity)

    def move(self):
        """
        Moving logic for the elevator: Take on request that is on the closest
        floor in the direction of movement. If there are no requests in the
        direction of movement, change direction.

        Return: Number of floors travelled
        """
        # Find closest request in each direction
        closest_up_request = float('inf')
        closest_down_request = float(-1)

        for passenger in self.requests:
            if passenger.at_destination:
                continue

            if passenger.in_elevator:
                # For passengers in the elevator get destination floor
                floor_request = passenger.destination
            else:
                # For passengers outside the elevator get pickup floor
                floor_request = passenger.current

            # Check direction of request and if it's closer than the current closest
            if floor_request > self.curr_floor and floor_request < closest_up_request:
                closest_up_request = floor_request
            elif floor_request < self.curr_floor and floor_request > closest_down_request:
                closest_down_request = floor_request

        prev_floor = self.curr_floor

        # Move to closest floor and update direction if needed
        if self.direction == self.DIRECTION_UP:
            if closest_up_request != float('inf'):
                self.curr_floor = closest_up_request
            else:
                self.direction = self.DIRECTION_DOWN
                self.curr_floor = closest_down_request
        else:
            if closest_down_request != float(-1):
                self.curr_floor = closest_down_request
            else:
                self.direction = self.DIRECTION_UP
                self.curr_floor = closest_up_request

        return abs(prev_floor - self.curr_floor)

