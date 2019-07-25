import math
import random


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
        # Get the coordinates of current position:
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
    width: size along the x dimension
    height: size along the y dimension
    all_times: a list contains the tuples which are coordinates of the tiles
    (which correspondslower left vertex)
    cleaned: the list contains the coordinates of cleaned tiles.
    num_obs: number of obstacles present in the room
    obstacles: list of tuples contain the coordinates of obstacles.
    empty_tiles: list of tuples contain the coordinates of empty tiles.

    """

    def __init__(self, width=5, height=5, num_obs=5):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.
        """
        self.width = width
        self.height = height
        self.all_tiles = [(x, y) for x in range(width) for y in range(height)]
        self.cleaned = []
        self.num_obs = num_obs

        self.obstacles = random.sample(self.all_tiles, self.num_obs)
        self.empty_tiles = [x for x in self.all_tiles if x not in self.obstacles]

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position pos as cleaned.
        Assumes that POS represents a valid position inside this room.
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        if (x, y) not in self.cleaned:
            self.cleaned.append((x, y))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.
        Assumes that (m, n) represents a valid tile inside the room.
        """
        return (m, n) in self.cleaned

    def getAllTiles(self):
        """
        Return a list of positions of all tiles on the board.
        """
        return self.all_tiles

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        """
        return self.width * self.height

    def getNumEmptyTiles(self):
        """
        Return the total number of tiles in the room.
        """
        return self.width * self.height - self.num_obs

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        """
        return len(self.cleaned)

    def getRandomPosition(self):
        """
        Return a random position inside the room.
        """
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        pos = Position(x, y)
        return pos

    def getRandomEmptyPosition(self):
        """
        Return a random position that is not an obstacle.
        """
        pos = random.choice(self.empty_tiles)
        pos = Position(pos[0], pos[1])
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.
        """
        return (0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height)

    def getListObstacles(self):
        """
        Return a list of obstacle positions
        """
        return self.obstacles

    def isObstacle(self, pos):
        # Check if the position lies on an obstacle
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        result = (x, y) in self.obstacles
        return result