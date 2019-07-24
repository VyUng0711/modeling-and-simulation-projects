import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from simulation import SimulationEngine
from elevators import ElevatorTypes


def test_strategy_by_passengers(total_floors, strategy):
    """
    Runs a strategy with different number of passengers
    """
    tests = {}
    capacity = 5

    for i in range(0, 1100, 100):
        total_passengers = i
        average = []

        # Run simulation 10 times and take the average
        for j in range(10):
            simulation = SimulationEngine(total_floors, total_passengers,
                                          strategy, capacity, False)
            result = simulation.run()
            average.append(result)
            simulation.reset()

        tests[i] = np.mean(average)
    return (tests)


def test_strategy_by_floors(num_passengers, strategy):
    """
    Runs a strategy with different number of floors
    """
    tests = {}
    capacity = 5

    for i in range(0, 1100, 100):
        total_floors = i
        average = []

        if total_floors == 0:
            tests[i] = 0
            continue

        # Run simulation 10 times and take the average
        for j in range(10):
            simulation = SimulationEngine(total_floors, num_passengers,
                                          strategy, capacity, False)
            result = simulation.run()
            average.append(result)
            simulation.reset()

        tests[i] = np.mean(average)
    return (tests)


def test_strategy_by_capacity(strategy):
    """
    Runs a strategy with different capacity size
    """
    tests = {}
    total_floors = 1000
    num_passengers = 1000

    for i in range(1, 1100, 100):
        capacity = i
        average = []

        # Run simulation 10 times and take the average
        for j in range(10):
            simulation = SimulationEngine(total_floors, num_passengers,
                                          strategy, capacity, False)

            result = simulation.run()
            average.append(result)
            simulation.reset()

        tests[i] = np.mean(average)
    return (tests)


def plot_floor_comparison(shabbat, ordinary, comparison_type=None):
    """
    Plot comparisons between 2 strategies
    """
    sns.set_style("darkgrid")

    if comparison_type not in ['num_passengers', 'floors', 'capacity']:
        raise ValueError("comparison_type must be one of 'num_passengers', 'floors'")

    if comparison_type == 'num_passengers':
        TITLE = "Average time as a function of no. of passengers"
        XLAB = "No. of passengers"

    elif comparison_type == 'floors':
        TITLE = "Average time as a function of no. of floors"
        XLAB = "No. of floors in building"

    # sorted by key, return a list of tuples
    list1 = sorted(ordinary.items())
    list2 = sorted(shabbat.items())

    # plot
    x1, y1 = zip(*list1)  # Ordinary
    plt.plot(x1, y1, c='green', label="ordinary")

    x2, y2 = zip(*list2)  # Shabbat
    plt.plot(x2, y2, c='blue', label="shabbat")

    plt.title(TITLE, fontsize=18)
    plt.xlabel(XLAB, fontsize=14)
    plt.ylabel('Average time', fontsize=14)
    plt.legend(loc=2)
    plt.show()


# Compare strategies as the number of passengers increases
shabbat = test_strategy_by_passengers(total_floors=10, strategy=ElevatorTypes.shabbat)
ordinary = test_strategy_by_passengers(total_floors=10, strategy=ElevatorTypes.ordinary)
plot_floor_comparison(shabbat, ordinary, comparison_type='num_passengers')

# Compare strategies as the number of floors increases
shabbat = test_strategy_by_floors(num_passengers=50, strategy=ElevatorTypes.shabbat)
ordinary = test_strategy_by_floors(num_passengers=50, strategy=ElevatorTypes.ordinary)
plot_floor_comparison(shabbat, ordinary, comparison_type='floors')
