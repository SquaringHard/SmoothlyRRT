import pygame as pg
from pygame.locals import *
from configs import *
from BasicFunction import *
from GenerateGraphs import *
from UpdateScreen import *

ObstaclePos = [START, None]
obstacles = []
results = GenerateGraphs(START, GOAL, obstacles)

pg.init()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption('S-RRT')

FlagRunning = True
FlagAddObstacle = False
FlagS_RRT = True

while FlagRunning:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            # Press SPACE to switch between Traditional RRT and S-RRT
            if event.key == K_SPACE:
                FlagS_RRT = not FlagS_RRT
            # Press ESC to exit simulation
            elif event.key == K_ESCAPE:
                FlagRunning = False

        elif event.type == MOUSEBUTTONDOWN:
            # Middle click to clear obstacles
            if event.button == 2:
                obstacles = []
            # Right click to generate results
            elif event.button == 3:
                results = GenerateGraphs(START, GOAL, obstacles)
            # Left click to add obstacles
            elif event.button == 1:
                ObstaclePos[FlagAddObstacle] = pg.mouse.get_pos()
                if FlagAddObstacle:
                    # Add the big obstacle by dividing it into smaller obstacles and add them
                    SmallObsPos = list(ObstaclePos[0])
                    ObstacleLen = CalcDist(ObstaclePos[0],ObstaclePos[1])
                    NumOfObs = int(ObstacleLen / EPS)
                    dxObs = (ObstaclePos[1][0] - ObstaclePos[0][0]) / NumOfObs
                    dyObs = (ObstaclePos[1][1] - ObstaclePos[0][1]) / NumOfObs
                    for i in range(NumOfObs):
                        obstacles.append(tuple(SmallObsPos))
                        SmallObsPos[0] += dxObs
                        SmallObsPos[1] += dyObs
                    ObstaclePos[0] = START
                FlagAddObstacle = not FlagAddObstacle

    UpdateScreen(SCREEN, START, GOAL, ObstaclePos, obstacles, FlagS_RRT, results)
    clock.tick(24)
