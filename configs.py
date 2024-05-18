import math

# The range of state space
[WIDTH, HEIGHT] = [1000, 600]
# The radius of the obstacle
OBSTACLES_RADIUS = 20
# Distance between small obstacles
EPS = OBSTACLES_RADIUS / 2

# Start and end points
START = (30, HEIGHT/2)
GOAL = (WIDTH-30, HEIGHT/2)

# RRT coefficients
P_GOAL = 0.6
THETA_THRESHOLD = 0.5 * math.pi
STEP_LEN = 20
MAX_NUM_OF_POINTS = 1e3

# B-Spline coefficients
NUM_OF_POINTS = 100
K_ORDER = 2

# RGB values
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [190, 190, 190]
RED = [240, 65, 85]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]