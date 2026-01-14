import datetime

import numpy as np
import math

import pymap3d
import pymap3d as map


# =====================
# Constants
# =====================
MU = 3.986004418e14          # Earth gravitational parameter [m^3/s^2]
R_E = 6378137.0              # Earth radius [m]
OMEGA_E = np.array([0.0, 0.0, 7.2921159e-5])  # Earth rotation [rad/s]
G0 = 9.80665                 # Sea-level gravity [m/s^2]


## RCS map takes in a map of az and el values rcsData[az][el] at a step size
class RCSMapAzEl:
    def __init__(self, mapOfValues, precision,azShift):
        self.rcsData = mapOfValues
        self.Precision = precision
        self.azShift = azShift

    def Value(self, targetState, observerState):

        targetPos = np.array([targetState.Pos.x,targetState.Pos.y,targetState.Pos.z])
        targetVel = np.array([targetState.Vel.x,targetState.Vel.y,targetState.Vel.z])
        observerPos = np.array([observerState.x,observerState.y,observerState.z])
        
        targetPointing = targetPos / np.linalg.norm(targetPos)
        dPos = -targetPos + observerPos
        posPointing = dPos / np.linalg.norm(dPos)
        velPointing = targetVel / np.linalg.norm(targetVel)
        x = np.dot(posPointing,velPointing)

        yUnit = np.cross(velPointing,-targetPointing)
        yUnit = yUnit / np.linalg.norm(yUnit)

        zUnit = np.cross(velPointing, yUnit)
        zUnit = zUnit/np.linalg.norm(zUnit)

        y = np.dot(posPointing,yUnit)
        z = np.dot(posPointing,zUnit)

        az = np.atan2(y,x)*180/math.pi
        el = np.atan2(z,math.sqrt(x*x+y*y)) * 180/math.pi
        el1 = el

        az = (az - self.azShift) % 180
        az1 = az
        val = 0.0
        count = 0.0

        az = int(az / self.Precision) * self.Precision
        el = int(el / self.Precision) * self.Precision

        azSign = 1
        elSign = 1
        dAz = (az1 - az) / self.Precision
        dEl = (el1 - el) / self.Precision

        if dAz < 0:
            azSign = -1
            dAz = math.fabs(dAz)

        if dEl < 0:
            elSign = -1
            dEl = math.fabs(dEl)

        q00 = self.rcsData[math.fabs(az)][math.fabs(el)]
        q01 = self.rcsData[math.fabs(az)][math.fabs(el + elSign * self.Precision)]
        q10 = self.rcsData[math.fabs(az + azSign * self.Precision)][math.fabs(el)]
        q11 = self.rcsData[math.fabs(az + azSign * self.Precision)][math.fabs(el + elSign * self.Precision)]

        azScale1 = dAz * q10 + (1-dAz) * q00
        azScale2 = dAz * q11 + (1-dAz) * q01


        elScale = dEl*azScale2+(1-dEl)*azScale1


        return elScale, az1, el1

    def Direct(self, az1, el1):
        az = int(az1 * self.Precision)
        el = int(el1 * self.Precision)
        print(az, el, az1, el1)
        return self.rcsData[math.fabs(az)][math.fabs(el)], az1, el1

class RCSAlgorithm:
    def __init__(self, scale):
        self.scale = scale

    def Value(self, targetState, observerState):
        targetPos = np.array([targetState.Pos.x, targetState.Pos.y, targetState.Pos.z])
        targetVel = np.array([targetState.Vel.x, targetState.Vel.y, targetState.Vel.z])
        observerPos = np.array([observerState.x, observerState.y, observerState.z])

        targetPointing = targetVel / np.linalg.norm(targetVel)
        dPos = observerPos - targetPos
        posPointing = dPos / np.linalg.norm(dPos)

        return self.scale*(1-np.abs(np.dot(targetPointing, posPointing)))

class RCSSphere:

    def Value(self, targetState, observerState):

        return 5



class Gravitational:
    def __init__(self):
        # Constants
        self.R_EARTH = 6371000  # Earth radius in meters
        self.G = 6.67430e-11  # Gravitational constant
        self.M_EARTH = 5.972e24  # Earth mass in kg
        self.MU = self.G * self.M_EARTH  # Standard gravitational parameter

    def CalcAccel(self, Pos):
        pos = [Pos.x,Pos.y, Pos.z]
        r = np.linalg.norm(pos)
        
        return -self.MU * np.array(pos) / (r**3)

class Vec:
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.t = t



class StateVector:
    def __init__(self,Pos:Vec, Vel:Vec):
        self.Pos = Pos
        self.Vel = Vel


class Obj:
    def __init__(self, rcsInfo, propagator):
        self.rcs = rcsInfo
        self.Propagator = propagator

    def Record(self, observerState):
        State = self.Propagator.StateInfo()
        return [State.Pos.x,State.Pos.y,State.Pos.z, State.Vel.x,State.Vel.y,State.Vel.z,State.Pos.t, self.rcs.Value(State, observerState)]

    def StateInfo(self):
        return self.Propagator.StateInfo()

    def Propagate(self,time):

        return self.Propagator.Propagate(time)
