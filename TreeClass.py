import random
from configs import *
from BasicFunction import *
from math import inf

# Used to store the generated random tree
class TreeClass:
    def __init__(self):
        self.points = [START]
        self.parent = {START: None}

    # This is also the randomly-generating-point function
    def SamplePoint(self, goal, PGoal):
        return goal if random.random() < PGoal else (random.randrange(WIDTH), random.randrange(HEIGHT))

    def AddPoint(self, point, parent):
        self.points.append(point)
        self.parent[point] = parent

    def FindNearestPoint(self, point):
        NearestPoint = self.points[0]
        NearestDist = inf
        
        for CandidatePoint in self.points:
            dist = CalcDist(point, CandidatePoint)
            if dist < NearestDist:
                NearestPoint = CandidatePoint
                NearestDist = dist

        return NearestPoint

    def FindPath(self):
        path = [GOAL]
        while path[-1] != START:
            # If a point is found to have no parent node during tracing, None will be returned
            if path[-1] not in self.parent:
                return None

            path.append(self.parent[path[-1]])

        path.reverse()
        return path

    # Adjust the path, remove unnecessary nodes, and correct corners that are too small
    def OptimizePath(self, path, obstacles):
        StartIndex = 0
        OptimizedPath = [path[0]]
        for GoalIndex in range(1, len(path) - 1):
            if not CheckCollision(path[StartIndex], path[GoalIndex], obstacles) and CheckCollision(path[StartIndex], path[GoalIndex + 1], obstacles):
                    OptimizedPath.append(path[GoalIndex])
                    StartIndex = GoalIndex
        OptimizedPath.append(path[-1])

        if len(OptimizedPath) >= 3:
            for i in range(len(OptimizedPath) - 2):
                p0 = OptimizedPath[i]
                p1 = OptimizedPath[i + 1]
                p2 = OptimizedPath[i + 2]

                # If angle p0-p1-p2 < THETA_THRESHOLD, find a point in path so and insert it to OptimizedPath so that the new angle to be large enough
                if CalcTheta(p0, p1, p2) < THETA_THRESHOLD:
                    for j in range(len(path)):
                        if path[j] == p0:
                            index0 = j
                        if path[j] == p1:
                            index1 = j
                            break

                    for j in range(index0, index1 + 1):
                        InsertPoint = path[j]
                        if CalcTheta(p0, InsertPoint, p1) >= THETA_THRESHOLD and CalcTheta(InsertPoint, p1, p2) >= THETA_THRESHOLD:
                            OptimizedPath.insert(i + 1, InsertPoint)
                            break
        
        return OptimizedPath