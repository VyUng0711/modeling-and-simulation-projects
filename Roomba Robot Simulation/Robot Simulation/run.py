from robots import StandardRobot, WallFollowingRobot, RandomWalkRobot
from simulation import RobotVisualization
from room import RectangularRoom


def testRobotMovement(robot_type, room_type, delay=0.4):
    """
    Runs a simulation of a single robot of type robot_type in a 5x5 room.
    """
    room = room_type(5,5,5)
    obstacles = room.getListObstacles()
    robot = robot_type(room, 1)
    anim = RobotVisualization(1, 5, 5, obstacles, delay)
    while room.getNumCleanedTiles() < room.getNumEmptyTiles():
        robot.updatePositionAndClean()
        anim.update(room, [robot])

    anim.done()


def main():
    try:
        #User inputs type of robot:
        robot_type = input("What robot to run the simulation? Enter StandardRobot, RandomWalkRobot, or WallFollowingRobot: ")
        if robot_type == "StandardRobot":
            testRobotMovement(StandardRobot, RectangularRoom)
        elif robot_type == "RandomWalkRobot":
            testRobotMovement(RandomWalkRobot, RectangularRoom)
        elif robot_type == "WallFollowingRobot":
            testRobotMovement(WallFollowingRobot, RectangularRoom)
        else:
            print("Invalid input, please try again")
            main()

    except ValueError:
        print("Invalid input, please try again")
        main()

main()


# main(RandomWalkRobot, RectangularRoom)
#testRobotMovement(WallFollowingRobot, RectangularRoom)
#testRobotMovement(StandardRobot, RectangularRoom)

