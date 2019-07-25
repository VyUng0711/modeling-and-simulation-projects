import matplotlib.pyplot as plt
import numpy as np
import pylab

from robots import StandardRobot, WallFollowingRobot, RandomWalkRobot
from room import RectangularRoom


def Simulation(velocity, width, height, num_obs, min_coverage, robot_type):
    """
    Return total time steps it takes to clean the fraction min_coverage of the room:
    """
    total_time = 0
    room = RectangularRoom(width, height, num_obs)
    robot = robot_type(room, velocity)
    while min_coverage*room.getNumEmptyTiles() > room.getNumCleanedTiles() and total_time < 10000:
        robot.updatePositionAndClean()
        total_time +=1
    return total_time


def showHistResult(num_trials, velocity, width, height, num_obs, min_coverage, robot_type):
    if robot_type == StandardRobot:
        name = "Standard Robot"
    elif robot_type == WallFollowingRobot:
        name = "Wall Following Robot"
    else:
        name = "Random Walk Robot"
    times = []
    for i in range(num_trials):
        this_time = Simulation(velocity, width, height, num_obs, min_coverage, robot_type)
        #If this is the failure case where the robot got stuck in one corner
        #due to the arrangement of obstacles and the loop tends to go on forever,
        # we don't count it in our result.
        if this_time < 10000:
            times.append(this_time)
    times_array = np.array(times)
    mean_time = np.mean(times_array)
    # print (mean_time)
    # std_time = np.std(times_array)
    # print (std_time)
    # conf_int = [mean_time - std_time*1.96, mean_time + std_time*1.96]
    # print (conf_int)
    plt.hist(times, bins=range(min(times), max(times) + 5, 5))
    plt.title("Histogram on number of time steps to clean the area for " + name)
    pylab.xlabel("Number of time steps to clean the area")
    pylab.show()

def centralLimit(sample_size, num_trials, robot_type):
    if robot_type == StandardRobot:
        name = "Standard Robot"
    elif robot_type == WallFollowingRobot:
        name = "Wall Following Robot"
    else:
        name = "Random Walk Robot"
    mean_samples = []
    for i in range(num_trials):
        this_trial_times = []
        for j in range(sample_size):
            this_time = Simulation(1, 5, 5, 5, 0.8, robot_type)
            this_trial_times.append(this_time)
        this_trial_mean = sum(this_trial_times)/len(this_trial_times)
        mean_samples.append(this_trial_mean)
    mean_samples = np.array(mean_samples)
    mean = np.mean(mean_samples)
    print ("Mean: ", mean)
    std = np.std(mean_samples)
    print ("Standard deviation: ", std)
    conf_int = [mean - std*1.96, mean + std*1.96]
    print (conf_int)
    plt.hist(mean_samples, bins=range(min(mean_samples), max(mean_samples) + 5, 5))
    plt.title("Distribution of the sample means for " + name)
    plt.axvline(x = conf_int[0], color='red')
    plt.axvline(x = conf_int[1], color='red')
    plt.xlabel("Sample means")
    plt.show()


def sim_average_time(velocity, width, height, num_obs, min_coverage, num_trials, robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.
    """
    totaltime = 0
    for i in range(num_trials):
        this_time = Simulation(velocity, width, height, num_obs, min_coverage, robot_type)
        totaltime += this_time
    return float(totaltime/num_trials)


def showPlot1():
    num_ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
    width = 5
    height = 5
    num_obstacle = [int(width*height*x) for x in num_ratios]
    #print (num_obstacle)
    #num_obstacle = range(0, 20)
    times1 = []
    times2 = []
    times3 = []
    for num in num_obstacle:
        print ("Plotting cleaning time for a room with {} of obstacles".format(num))
        times1.append(sim_average_time(1, width, height, num, 0.8, 100, StandardRobot))
        times2.append(sim_average_time(1, width, height, num, 0.8, 100, RandomWalkRobot))
        times3.append(sim_average_time(1, width, height, num, 0.8, 100, WallFollowingRobot))
    pylab.plot(num_ratios, times1)
    pylab.plot(num_ratios, times2)
    pylab.plot(num_ratios, times3)
    pylab.title("Plot on how effective the strategies are \n given the proportion of the room that is occupied by obstacles")
    pylab.legend(('StandardRobot', 'RandomWalkRobot','WallFollowingRobot'))
    pylab.xlabel("Proportion that is occupied by obstacles")
    pylab.ylabel("Average time needed")
    pylab.show()

#showPlot1()

def showPlot2():
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [20, 25, 50, 60, 100]:
        height = 300/width
        num_obstacle = int(width*height*0.1)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(sim_average_time(1, width, height, num_obstacle, 0.8, 100, StandardRobot))
        times2.append(sim_average_time(1, width, height, num_obstacle, 0.8, 100, RandomWalkRobot))
        times3.append(sim_average_time(1, width, height, num_obstacle, 0.8, 100, WallFollowingRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.plot(aspect_ratios, times3)
    pylab.title('Plot on how effective the strategies are given different aspect ratios')
    pylab.legend(('StandardRobot', 'RandomWalkRobot', 'WallFollowingRobot'))
    pylab.xlabel('aspect_ratios')
    pylab.ylabel('time')
    pylab.show()

#showPlot2()

def showPlot3():
    min_coverage = [0.2, 0.4, 0.6, 0.8, 1]
    times1 = []
    times2 = []
    times3 = []
    for c in min_coverage:
        print("Plotting cleaning time for coverage of {}".format(c))
        times1.append(sim_average_time(1, 5, 5, 5, c, 100, StandardRobot))
        times2.append(sim_average_time(1, 5, 5, 5, c, 100, RandomWalkRobot))
        times3.append(sim_average_time(1, 5, 5, 5, c, 100, WallFollowingRobot))
    pylab.plot(min_coverage, times1)
    pylab.plot(min_coverage, times2)
    pylab.plot(min_coverage, times3)
    pylab.title("Plot on how effective the strategies are given the min coverage")
    pylab.legend(('StandardRobot', 'RandomWalkRobot','WallFollowingRobot'))
    pylab.xlabel("Min coverage")
    pylab.ylabel("Average time needed")
    pylab.show()

#showPlot3()