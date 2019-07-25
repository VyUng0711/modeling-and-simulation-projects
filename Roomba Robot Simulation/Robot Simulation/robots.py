import random
from room import Position

class Robot(object):
    """
    Represents a robot cleaning a particular room.
    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed velocity.
    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean()
    """

    def __init__(self, room, velocity):
        """
        Initializes a Robot with the given velocity in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.
        """
        # Start from the middle of the room

        self.dir = int(360 * random.random())
        # Compment this line if starting from a random position
        # self.pos = room.getRandomEmptyPosition()
        # Start from coordinate (0,0) (lower left corner of the board)
        # self.pos = Position(0, 0)
        self.gap = 0
        self.visited_tile = []
        self.num_hit_walls = 0
        self.num_hit_obs = 0
        self.room = room
        self.pos = Position(self.room.width // 2, self.room.height // 2)

        if not self.room.isObstacle(self.pos):
            self.room.cleanTileAtPosition(self.pos)
        self.pastobstacle = False  # indicate whether the robot was about to hit an obstacle in the previous time step
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
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to position
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to direction
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.
    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it turns back (180 degree)
    """

    def updatePositionAndClean(self):
        new_pos = self.pos.getNewPosition(self.dir, self.velocity)
        if self.room.isObstacle(new_pos) or not self.room.isPositionInRoom(new_pos):
            self.dir = int(360 * random.random())
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
            # Follow the wall and continue with the same direction
            self.dir = self.dir + 90
            self.pastobstacle = True
        elif not self.room.isPositionInRoom(new_pos):
            self.dir = int(360 * random.random())
        else:
            if self.pastobstacle == True:
                self.dir = self.dir - 90
            self.pos = new_pos
            self.pastobstacle = False
            if len(self.visited_tile) == 0:
                self.visited_tile.append(self.pos)
            else:
                if self.pos.getX() == self.visited_tile[-1].getX() and self.pos.getY() == self.visited_tile[-1].getY():
                    self.gap += 1
                else:
                    self.visited_tile.append(self.pos)
            self.room.cleanTileAtPosition(self.pos)
            if self.gap > 10:
                self.dir = int(360 * random.random())
                self.gap = 0


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """

    def updatePositionAndClean(self):
        self.dir = int(360 * random.random())
        while not self.room.isPositionInRoom(self.pos.getNewPosition(self.dir, self.velocity)) \
                or self.room.isObstacle(self.pos.getNewPosition(self.dir, self.velocity)):
            self.dir = int(360 * random.random())
        self.pos = self.pos.getNewPosition(self.dir, self.velocity)
        self.room.cleanTileAtPosition(self.pos)