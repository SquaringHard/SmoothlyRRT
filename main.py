import pygame as pg
from pygame.locals import *
import Update

FlagRunning = True
while FlagRunning:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            # Press SPACE to switch between Traditional RRT and S-RRT
            if event.key == K_SPACE:
                Update.updateFlagS_RRT()
            # Press ESC to exit simulation
            elif event.key == K_ESCAPE:
                FlagRunning = False

        elif event.type == MOUSEBUTTONDOWN:
            # Middle click to clear obstacles
            if event.button == 2:
                Update.clearObstacles()
            # Right click to generate results
            elif event.button == 3:
                Update.updateResults()
            # Left click to add obstacles
            elif event.button == 1:
                Update.updateObstacles()

    Update.UpdateScreen()