import math

import Helper
import pymap3d as mp
import Types as T
import datetime
import Objects as O
import numpy as np

Deg2Rad = math.pi/180.0



# GenerateTrajectory will simulate and return a set of states
def GenerateTrajectory(object, startTime, stopTime, timeStep):

    tm = startTime
    states = []
    while tm < stopTime:
        _ = object.Propagate(tm)
        res = object.Record()

        targetPos = np.array([res[0], res[1], res[2]])
        targetVel = np.array([res[3], res[4], res[5]])

        locPoint = targetPos / np.linalg.norm(targetPos)
        xUnit = targetVel / np.linalg.norm(targetVel)

        yUnit = -np.cross(xUnit, locPoint)
        yUnit = yUnit / np.linalg.norm(yUnit)

        zUnit = np.cross(xUnit, yUnit)
        zUnit = zUnit / np.linalg.norm(zUnit)

        q0, q1, q2, q3 = Helper.ConvertUnitVecs2Qs(xUnit, yUnit, zUnit)

        # xUnit1, yUnit1, zUnit1 = Helper.ConvertQs2UnitVecs(q0,q1,q2,q3)
        # print("x: ",xUnit, xUnit1)
        # print("y: ", yUnit, yUnit1)
        # print("z: ", zUnit, zUnit1)

        states.append([res[-1], res[0], res[1], res[2], res[3], res[4], res[5], q0, q1, q2, q3])

        tm = tm + datetime.timedelta(seconds=timeStep)

    return states