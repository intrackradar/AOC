import datetime

import numpy as np
import math
import Helper as H
import pymap3d
import pymap3d as map


# =====================
# Constants
# =====================
MU = 3.986004418e14          # Earth gravitational parameter [m^3/s^2]
R_E = 6378137.0              # Earth radius [m]
OMEGA_E = np.array([0.0, 0.0, 7.2921159e-5])  # Earth rotation [rad/s]
G0 = 9.80665                 # Sea-level gravity [m/s^2]

class RCSMap:
    def __init__(self, rcsazelmaps, freqVals):
        self.RCSAzElMaps = rcsazelmaps
        self.FreqVals = freqVals
        self.MaxF = np.max(freqVals)
        self.MinF = np.min(freqVals)

    def Value(self, targetState, observerState, Freq):
        if Freq > self.MaxF*1.1:
            print("higher than max: ",Freq, self.MaxF)
            return [np.nan, 0, 0]
        if Freq < self.MinF*0.9:
            print("less than min: ", Freq, self.MinF)
            return [np.nan, 0, 0]

        ind = np.argmin(np.fabs(self.FreqVals - Freq))

        if ind == len(self.FreqVals) - 1 and Freq >= self.FreqVals[-1]:
            return self.RCSAzElMaps[-1].Value(targetState, observerState)
        if ind == 0 and Freq <= self.FreqVals[0]:
            return self.RCSAzElMaps[0].Value(targetState, observerState)

        q1 = self.RCSAzElMaps[ind].Value(targetState, observerState)
        q2 = 0
        scale = 0

        if Freq > self.FreqVals[ind]:
            q2 = self.RCSAzElMaps[ind+1].Value(targetState, observerState)
            scale = (Freq-self.FreqVals[ind])/(self.FreqVals[ind+1]-self.FreqVals[ind])
        else:
            q2 = self.RCSAzElMaps[ind - 1].Value(targetState, observerState)
            scale = 1-(Freq - self.FreqVals[ind-1]) / (self.FreqVals[ind] - self.FreqVals[ind-1])

        return q1[0]*(1-scale) + scale*q2[0], q1[1], q1[2]
## RCS map takes in a map of az and el values rcsData[az][el] at a step size
class RCSMapAzEl:
    def __init__(self, mapOfValues, azprecision, elprecision,azShift):
        self.rcsData = mapOfValues
        self.azPrecision = azprecision
        self.elPrecision = elprecision
        self.azShift = azShift

    def Value(self, targetState, observerState):

        targetPos = np.array([targetState.Pos.x,targetState.Pos.y,targetState.Pos.z])
        observerPos = np.array([observerState.x,observerState.y,observerState.z])
        
        dPos = -targetPos + observerPos
        obsPointing = dPos / np.linalg.norm(dPos)


        q0 = targetState.Qs[0]
        q1 = targetState.Qs[1]
        q2 = targetState.Qs[2]
        q3 = targetState.Qs[3]
        xUnit, yUnit, zUnit = H.ConvertQs2UnitVecs(q0, q1, q2, q3)

        x = np.dot(obsPointing, xUnit)
        y = np.dot(obsPointing, yUnit)
        z = np.dot(obsPointing, zUnit)

        az = np.atan2(y,x)*180/math.pi
        el = np.atan2(z,math.sqrt(x*x+y*y)) * 180/math.pi
        print("Value: az, el ", az, el)
        return self.GetRCS(az, el)

    def Direct(self, az1, el1):
        az = int(az1 * self.Precision)
        el = int(el1 * self.Precision)
        print(az, el, az1, el1)
        return self.rcsData[math.fabs(az)][math.fabs(el)], az1, el1

    def GetRCS(self, az, el):
        print("GetRCS", az, el)
        el1 = el
        az = (az - self.azShift)
        if az > 180:
            az = 360 - az

        if az < -180:
            az = -360 - az

        az1 = az
        val = 0.0
        count = 0.0

        az = int(az / self.azPrecision) * self.azPrecision
        el = int(el / self.elPrecision) * self.elPrecision

        azSign = 1
        elSign = 1
        dAz = (az1 - az) / self.azPrecision
        dEl = (el1 - el) / self.elPrecision

        if dAz < 0:
            azSign = -1
            dAz = math.fabs(dAz)

        if dEl < 0:
            elSign = -1
            dEl = math.fabs(dEl)

        q00 = 10**(self.rcsData[math.fabs(az)][math.fabs(el)]/10)
        q01 = 10**(self.rcsData[math.fabs(az)][math.fabs(el + elSign * self.elPrecision)]/10)
        q10 = 10**(self.rcsData[math.fabs(az + azSign * self.azPrecision)][math.fabs(el)]/10)
        q11 = 10**(self.rcsData[math.fabs(az + azSign * self.azPrecision)][math.fabs(el + elSign * self.elPrecision)]/10)

        azScale1 = dAz * q10 + (1 - dAz) * q00
        azScale2 = dAz * q11 + (1 - dAz) * q01

        elScale = dEl * azScale2 + (1 - dEl) * azScale1

        # print(dAz, dEl, elScale, q00, q10, q01, q11, 0.25*(q00+q01+q10+q11))
        print("Get RCS: az, el ", az, el, 10*math.log10(elScale))
        return 10*math.log10(elScale), az1, el1
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
    def __init__(self,Pos:Vec, Vel:Vec, Qs):
        self.Pos = Pos
        self.Vel = Vel
        self.Qs = Qs


class Obj:
    def __init__(self, name, rcsInfo, propagator):
        self.rcs = rcsInfo
        self.Propagator = propagator
        self.Name = name

    def Record(self):
        State = self.Propagator.StateInfo()
        return [State.Pos.x,State.Pos.y,State.Pos.z, State.Vel.x,State.Vel.y,State.Vel.z,State.Pos.t]

    def RecordFromObserver(self, observerState, freq):
        State = self.Propagator.StateInfo()
        return [State.Pos.x, State.Pos.y, State.Pos.z, State.Vel.x, State.Vel.y, State.Vel.z, State.Pos.t,
                self.rcs.Value(State, observerState, freq)]

    def StateInfo(self):
        return self.Propagator.StateInfo()

    def Propagate(self,time):

        return self.Propagator.Propagate(time)
