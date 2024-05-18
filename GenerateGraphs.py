import time
from configs import *
from RRT import *
from BSpline import *

def GenerateGraphs(start, goal, obstacles):
    t0 = time.time()

    # Generate paths using S-RRT
    tree = RRT(start, goal, obstacles, P_GOAL)
    path = tree.FindPath(start, goal)
    OptimizedPath = tree.OptimizePath(path, obstacles)
    
    # Use control points to generate B-spline curves as motion trajectories
    # Because we are using a third-order B-spline curve, the number of control points is required to be at least 3
    # So when there are only start and end points, add their midpoints as supplementary points
    if len(OptimizedPath) < 3:
        AddedPoint = (0.5 * (start[0] + goal[0]), 0.5 * (start[1] + goal[1]))
        OptimizedPath.append(AddedPoint)
    trajectory = GenerateBSpline(OptimizedPath)

    t1 = time.time()

    # Generate paths using RRT.
    TraditionalTree = RRT(start, goal, obstacles)
    TraditionalPath = TraditionalTree.FindPath(start, goal)

    t2 = time.time()
    
    print("Traditional RRT: {}\tnodes, {}\tseconds.".format(len(TraditionalTree.points),t1 - t0))
    print("S-RRT:           {}\tnodes, {}\tseconds.".format(len(tree.points),t2 - t1))
    return [trajectory, tree, path, OptimizedPath, TraditionalTree, TraditionalPath]