import math
import random

import pylab

import math
import time
import matplotlib.pyplot as plt
import numpy as np

try:
    # for Python2
    from Tkinter import *   
except ImportError:
    # for Python3
    from tkinter import *

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, velocity):
        """
        Computes and returns the new Position after one time step
        , with this object as the current position, and with the
        specified angle and velocity.
        Inputs: 
        angle: float representing angle in degrees 0 <= angle < 360
        velocity: positive float representing velocity 0 <= velocity <= 1
        Output: 
        a Position object representing the new position.
        """
        #Get the coordinates of current position:
        cur_x, cur_y = self.getX(), self.getY()
        # Compute the change in position
        # Because the unit for time is time step and it is always 1, we don't multiply time
        # when calculating delta_x and delta_y 
        delta_y = velocity * math.cos(math.radians(angle))
        delta_x = velocity * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = cur_x + delta_x
        new_y = cur_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles and obstacles. 
    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of the empty tiles is either clean or dirty.
    """
    def __init__(self, width=5, height=10, num_obs=4):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.
        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.all_tiles = [(x,y) for x in range(width) for y in range(height)]
        self.cleaned = []
        #self.percent_obs = percent_obs
        #self.num_obs = int(self.percent_obs*float(self.width)*float(self*height))
        self.num_obs = num_obs
        
        #self.obstacles = [(2,1),(1,2),(2,3),(3,2)]
        self.obstacles = random.sample(self.all_tiles, self.num_obs)
        self.empty_tiles = [x for x in (self.all_tiles) if x not in self.obstacles]

        
        # obs_xs = random.sample(range(self.width), num_obs)
        # obs_ys = random.sample(range(self.height), num_obs)
        # self.obstacles = [(obs_xs[i], obs_ys[i]) for i in range(int(percent_obs*self.width*self*height))]
  
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.
        pos: a Position
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        if (x,y) not in self.cleaned:
            self.cleaned.append((x,y))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.
        Assumes that (m, n) represents a valid tile inside the room.
        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m,n) in self.cleaned

    def getAllTiles(self):
        """
        Return a list of positions of all tiles on the board. 
        """
        return self.all_tiles

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        returns: an integer
        """
        return self.width * self.height

    def getNumEmptyTiles(self):
        """
        Return the total number of tiles in the room.
        returns: an integer
        """
        return (self.width * self.height - self.num_obs)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        returns: an integer
        """
        return len(self.cleaned)

    def getRandomPosition(self):
        """
        Return a random position inside the room.
        returns: a Position object.
        """
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        pos = Position(x,y)
        return pos

    def getRandomEmptyPosition(self):
        pos = random.choice(self.empty_tiles)
        pos = Position(pos[0], pos[1])
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.
        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height)

    def getListObstacles(self):
        """
        Return a list of obstacle positions
        """
        return self.obstacles

    def isObstacle(self, pos):
        #Check if the position lies on an obstacle
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        result = (x,y) in self.obstacles
        return (result)

# r = RectangularRoom(5, 5, 3)
# os = r.getListObstacles()

# point = random.choice(os)
# point = Position(point[0], point[1])
# print (point)
# print (os)
# print (r.isObstacle(point))


class Robot(object):
    """
    Represents a robot cleaning a particular room.
    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed velocity.
    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, velocity):
        """
        Initializes a Robot with the given velocity in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.
        room:  a RectangularRoom object.
        velocity: a float (velocity > 0)
        """
        #Start from the middle of the room
        
        self.dir = int(360 * random.random())
        #Compment this line if starting from a random position
        #self.pos = room.getRandomEmptyPosition()
        #Start from coordinate (0,0) (lower left corner of the board)
        #self.pos = Position(0, 0)
        self.gap = 0
        self.visited_tile = []
        self.num_hit_walls = 0
        self.num_hit_obs = 0
        self.room = room
        self.pos = Position(self.room.width//2, self.room.height//2)
        
        if not self.room.isObstacle(self.pos):
            self.room.cleanTileAtPosition(self.pos)
        self.pastobstacle = False #indicate whether the robot was about to hit an obstacle in the previous time step
        if velocity > 0:
            self.velocity = velocity
        else:
            raise ValueError("Velocity should be greater than zero")

    def getRobotPosition(self):
        """
        Return the position of the robot.
        returns: a Position object giving the robot's position.
        """
        return self.pos

    def getRobotDirection(self):
        """
        Return the direction of the robot.
        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.
        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.
        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.
    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it turns back (180 degree) 
    """
    # def __init__(self, room, velocity):
    #     Robot.__init__(self, room, velocity)
    #     self.name = "Standard Robot"
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_pos = self.pos.getNewPosition(self.dir, self.velocity)
        #print (new_pos)
        if self.room.isObstacle(new_pos) or not self.room.isPositionInRoom(new_pos):
            self.dir = int(360 * random.random())
        # if self.room.isObstacle(new_pos)
        #     #Drawback of this approach is that if the robot is stuck between two obstacle
        #     #that are close to each other, it would never get out of the loop.
        #     new_dir = self.dir + 180
        #     self.dir = new_dir 
        #     #print ('Face obstacle')
        # elif not self.room.isPositionInRoom(new_pos):
        #     self.dir = int(360 * random.random())
            #print ('Position not in room')
        else:
            self.pos = new_pos
            self.room.cleanTileAtPosition(self.pos)

class WallFollowingRobot(Robot):
    """
    A WallFollowingRobot is a robot with the "wall following " movement strategy: when facing a wall, 
    it will turn 90 degree to the right, move one step forward and then turn 90 degree to the left to 
    maintain the original direction, which means it basically just avoid the wall instead of turning back. 
    """
    def updatePositionAndClean(self):
        new_pos = self.pos.getNewPosition(self.dir, self.velocity)
        if self.room.isObstacle(new_pos):
            #Follow the wall and continue with the same direction
            self.dir = self.dir + 90
            self.pastobstacle = True
            #print ('Face obstacle')
        elif not self.room.isPositionInRoom(new_pos):
            self.dir = int(360 * random.random())
            #print ('Position not in room')
        else:
            if self.pastobstacle == True:
                self.dir = self.dir - 90
            self.pos = new_pos
            self.pastobstacle = False
            if len(self.visited_tile) == 0:
                self.visited_tile.append(self.pos)
            else:
                if self.pos.getX() == self.visited_tile[-1].getX() and self.pos.getY() == self.visited_tile[-1].getY():
                    self.gap +=1 
                else:
                    self.visited_tile.append(self.pos)
            self.room.cleanTileAtPosition(self.pos)
            if self.gap > 10:
                self.dir = int(360 * random.random())
                self.gap = 0
            # else:
            #     if self.pastobstacle == True:
            #         self.dir = self.dir - 90

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.dir = int(360 * random.random())
        new_pos = self.pos.getNewPosition(self.dir, self.velocity)
        while not self.room.isPositionInRoom(new_pos) or self.room.isObstacle(new_pos):
            self.dir = int(360 * random.random())
        self.pos = new_pos
        self.room.cleanTileAtPosition(self.pos)

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
    print (mean_time)
    std_time = np.std(times_array)
    print (std_time)
    conf_int = [mean_time - std_time*1.96, mean_time + std_time*1.96]
    print (conf_int)
    plt.hist(times, bins=range(min(times), max(times) + 5, 5))
    #ylim = plt.ylim()[1]
    plt.title("Histogram on number of time steps to clean the area for " + name)
    plt.axvline(x = conf_int[0], color='red')
    plt.axvline(x = conf_int[1], color='red')
    pylab.ylabel("Number of time steps to clean the area")
    pylab.show()

#showHistResult(100000, 1, 5, 5, 5, 0.8, StandardRobot)
#showHistResult(100000, 1, 5, 5, 5, 0.8, RandomWalkRobot)
#showHistResult(100000, 1, 5, 5, 5, 0.8, WallFollowingRobot)
#print(Simulation(1, 5, 5, 5, 0.8, StandardRobot))
#print(Simulation(1, 5, 5, 5, 0.8, RandomWalkRobot))
#print(Simulation(1, 5, 5, 5, 0.8, WallFollowingRobot))


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


# times = []
# num_obstacles = range(0,5)
# for num in num_obstacles:
#     times.append(sim_average_time(1, 4, 5, num, 0.8, 5, StandardRobot))
# print (times)

#print (sim_average_time(1, 4, 5, 4, 0.8, 5, StandardRobot))



def showPlot1():
    num_ratios = [0.1, 0.2, 0.3, 0.4, 0.5]
    width = 5
    height = 5
    num_obstacle = [int(width*height*x) for x in num_ratios]
    print (num_obstacle)
    #num_obstacle = range(0, 20)
    times1 = []
    times2 = []
    times3 = []
    for num in num_obstacle:
        print ("Plotting cleaning time for a room with {} obstacles".format(num))
        times1.append(sim_average_time(1, width, height, num, 0.8, 100, StandardRobot))
        times2.append(sim_average_time(1, width, height, num, 0.8, 100, RandomWalkRobot))
        times3.append(sim_average_time(1, width, height, num, 0.8, 100, WallFollowingRobot))
    pylab.plot(num_ratios, times1)
    pylab.plot(num_ratios, times2)
    pylab.plot(num_ratios, times3)
    pylab.title("Plot on how effective the strategies are \n given the proportion of the room that is occupied by obstacles")
    pylab.legend(('StandardRobot', 'RandomWalkRobot','WallFollowingRobot'))
    pylab.xlabel("Number of obstacles")
    pylab.ylabel("Average time needed")
    pylab.show()

#showPlot1()

def showPlot2():
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
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
    min_coverage = [0.2, 0.4, 0.6, 0.8]
    times1 = []
    times2 = []
    times3 = []
    for c in min_coverage:
        print ("Plotting cleaning time for coverage of {}".format(c))
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


# def sim_average_time(num_robots, velocity, width, height, min_coverage, num_trials,
#                   robot_type):
#     """
#     Runs NUM_TRIALS trials of the simulation and returns the mean number of
#     time-steps needed to clean the fraction MIN_COVERAGE of the room.
#     The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
#     velocity velocity, in a room of dimensions WIDTH x HEIGHT.
#     num_robots: an int (num_robots > 0)
#     velocity: a float (velocity > 0)
#     width: an int (width > 0)
#     height: an int (height > 0)
#     min_coverage: a float (0 <= min_coverage <= 1.0)
#     num_trials: an int (num_trials > 0)
#     robot_type: class of robot to be instantiated (e.g. StandardRobot or
#                 RandomWalkRobot)
#     """
#     totaltime = 0
#     num = num_trials
#     while num>0:
#         #anim = ps7_visualize.RobotVisualization(num_robots, width, height)
#         room = RectangularRoom(width, height)
#         i = num_robots
#         robots= []
#         while i>0:
#             robots.append(robot_type(room, velocity))
#             i -= 1
#         while min_coverage * room.getNumTiles() > room.getNumCleanedTiles():
#             for robot in robots:
#                 robot.updatePositionAndClean()
#             totaltime += 1
#         #    anim.update(room, robots)
#         num -= 1
#         #anim.done()
#     return float(totaltime/num_trials)



# def showPlot1(title, x_label, y_label):
#     """
#     What information does the plot produced by this function tell you?
#     """
#     num_robot_range = range(1, 11)
#     times1 = []
#     times2 = []
#     for num_robots in num_robot_range:
#         print ("Plotting", num_robots, "robots...")
#         times1.append(sim_average_time(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
#         times2.append(sim_average_time(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
#     pylab.plot(num_robot_range, times1)
#     pylab.plot(num_robot_range, times2)
#     pylab.title(title)
#     pylab.legend(('StandardRobot', 'RandomWalkRobot'))
#     pylab.xlabel(x_label)
#     pylab.ylabel(y_label)
#     pylab.show()

    
# def showPlot2(title, x_label, y_label):
#     """
#     What information does the plot produced by this function tell you?
#     """
#     aspect_ratios = []
#     times1 = []
#     times2 = []
#     for width in [10, 20, 25, 50]:
#         height = 300/width
#         print ("Plotting cleaning time for a room of width:", width, "by height:", height)
#         aspect_ratios.append(float(width) / height)
#         times1.append(sim_average_time(2, 1.0, width, height, 0.8, 200, StandardRobot))
#         times2.append(sim_average_time(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
#     pylab.plot(aspect_ratios, times1)
#     pylab.plot(aspect_ratios, times2)
#     pylab.title(title)
#     pylab.legend(('StandardRobot', 'RandomWalkRobot'))
#     pylab.xlabel(x_label)
#     pylab.ylabel(y_label)
#     pylab.show()



class RobotVisualization:
    def __init__(self, num_robots, width, height, obstacles, delay = 0.2):
        "Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.num_robots = num_robots

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gray squares for dirty tiles
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,
                                                             fill = "gray")
        #Draw red squares for obstacles:
        self.obstacles = {}
        for o in obstacles:
            x1, y1 = self._map_coords(o[0], o[1])
            x2, y2 = self._map_coords(o[0]+1, o[1]+1)
            self.obstacles[(o[0],o[1])] = self.w.create_rectangle(x1, y1, x2, y2, fill="red")

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
        self.robots = None
        self.text = self.w.create_text(25, 0, anchor=NW,
                                       text=self._status_string(0, 0))
        self.time = 0
        self.master.update()

    def _status_string(self, time, num_clean_tiles):
        "Returns an appropriate status string to print."
        percent_clean = 100 * num_clean_tiles / (self.width * self.height - len(self.obstacles))
        return "Time: %04d; %d tiles (%d%%) cleaned" % \
            (time, num_clean_tiles, percent_clean)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_robot(self, position, direction):
        "Returns a polygon representing a robot with the specified parameters."
        x, y = position.getX(), position.getY()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 0.6 * math.sin(math.radians(d1)),
                                  y + 0.6 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 0.6 * math.sin(math.radians(d2)),
                                  y + 0.6 * math.cos(math.radians(d2)))
        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")

    def update(self, room, robots):
        "Redraws the visualization with the specified room and robot state."
        # Removes a gray square for any tiles have been cleaned.
        for i in range(self.width):
            for j in range(self.height):
                if room.isTileCleaned(i, j):
                    self.w.delete(self.tiles[(i, j)])
        # Delete all existing robots.
        if self.robots:
            for robot in self.robots:
                self.w.delete(robot)
                self.master.update_idletasks()
        # Draw new robots
        self.robots = []
        for robot in robots:
            pos = robot.getRobotPosition()
            x, y = pos.getX(), pos.getY()
            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
            self.robots.append(self.w.create_oval(x1, y1, x2, y2,
                                                  fill = "black"))
            self.robots.append(
                self._draw_robot(robot.getRobotPosition(), robot.getRobotDirection()))
        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(
            25, 0, anchor=NW,
            text=self._status_string(self.time, room.getNumCleanedTiles()))
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()


def testRobotMovement(robot_type, room_type, delay = 0.4):
    """
    Runs a simulation of a single robot of type robot_type in a 5x5 room.
    """
    room = room_type(10,10,25)
    obstacles = room.getListObstacles()
    robot = robot_type(room, 1)
    anim = RobotVisualization(1, 10, 10, obstacles, delay)
    while room.getNumCleanedTiles() < room.getNumEmptyTiles():
        robot.updatePositionAndClean()
        anim.update(room, [robot])

    anim.done()

#testRobotMovement(StandardRobot, RectangularRoom)
#testRobotMovement(WallFollowingRobot, RectangularRoom)
testRobotMovement(RandomWalkRobot, RectangularRoom)

#def sim_average_time(velocity, width, height, num_obs, min_coverage, num_trials, robot_type):


