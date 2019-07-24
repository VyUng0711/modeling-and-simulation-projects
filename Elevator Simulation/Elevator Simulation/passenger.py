import numpy as np


class Passenger():
    """
    Class representing the Passenger entity in the simulation

    Attributes:
        id: unique identified of passenger
        current: The floor which the passenger comes from
        destination: The floor which the passenger wants to go to
        in_elevator: Is passenger currently in the elevator or waiting outside
        at_destination: Is passenger delivered to their destination
    """

    DEFAULT_IS_INSIDE = False
    DEFAULT_AT_DESTINATION = False

    def __init__(self, index, num_floors):
        self.id = index

        journey = self._assign_journey(num_floors)
        self.current = journey[0]
        self.destination = journey[1]

        self.in_elevator = self.DEFAULT_IS_INSIDE
        self.at_destination = self.DEFAULT_AT_DESTINATION

    def _assign_journey(self, num_floors):
        """
        Output starting floor and ending floor, making sure that they differ,
        and biasing towards starting or ending at the lobby.
        """
        curr = [0 if np.random.random() < 0.5
                  else np.random.randint(1, num_floors)]

        dest = [0 if np.random.random() < 0.5
                  else np.random.randint(1, num_floors)]

        # Ensure that current floor != destination floor
        while curr == dest:
            dest = [0 if np.random.random() < 0.5
                      else np.random.randint(1, num_floors)]

        return(curr[0], dest[0])

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return repr(self)