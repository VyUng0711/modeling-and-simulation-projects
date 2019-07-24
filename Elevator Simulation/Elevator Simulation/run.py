from simulation import SimulationEngine
from elevators import ElevatorTypes


def main():
    try:
        #User inputs number of passengers and number of floors
        total_passengers = int(input("How many passengers are there?: "))
        total_floors = int(input("How many floors are there?: "))
        capacity = int(input("How many passengers can fit in the elevator?: "))

        simulation = SimulationEngine(total_floors, total_passengers,
                                        ElevatorTypes.ordinary, capacity)

        simulation.run()

    except ValueError:
        print("Invalid input, please try again")
        main()

main()