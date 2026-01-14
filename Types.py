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


class BasicPropagator:
    def __init__(self, startState, dt, accelModel):
        self.dt = dt
        self.accelModel = accelModel
        self.State = startState

    def StateInfo(self):
        return self.State

    def Propagate(self, time):
        while self.State.Pos.t < time:
            incrementTime = self.State.Pos.t
            if self.State.Pos.t + self.dt > time:
                incrementTime = time
            else:
                incrementTime = incrementTime+self.dt
            self.StepTo(incrementTime)
        return self.StateInfo()

    def StepTo(self,time):

        llh = map.ecef2geodetic(self.State.Pos.x, self.State.Pos.y, self.State.Pos.z)
        if llh[2] < 0:
            self.State.Pos.t = time
            return
        dt = time - self.State.Pos.t

        Accel = self.AccelModel.CalcAccel(self.State.Pos)

        self.State.Pos.x = self.State.Pos.x + dt * self.State.Vel.x + 0.5*dt*dt*Accel[0]
        self.State.Pos.y = self.State.Pos.y + dt * self.State.Vel.y + 0.5*dt*dt*Accel[1]
        self.State.Pos.z = self.State.Pos.z + dt * self.State.Vel.z + 0.5*dt*dt*Accel[2]
        self.State.Pos.t = time


        self.State.Vel.x = self.State.Vel.x + dt * Accel[0]
        self.State.Vel.y = self.State.Vel.y + dt * Accel[1]
        self.State.Vel.z = self.State.Vel.z + dt * Accel[2]
        self.State.Vel.t = time

class stage:
    def __init__(self, fuelMass, thrust, isp):
        self.isp = isp
        self.fuelMass = fuelMass
        self.thrust = thrust
    def Thrust(self):
        return self.thrust

    def Burn(self, dt):
        if self.fuelMass <= 0:
            return

        mdot = -self.thrust / (self.isp * 9.80665)

        self.fuelMass = self.fuelMass + dt * mdot

    def HasFuel(self):
        if self.fuelMass > 0:
            return True

        return False

    def Fuel(self):
        return np.fmax(self.fuelMass, 0.0)

class Heading:
    def __init__(self,timeRange,pointing):
        self.TR = timeRange
        self.P = pointing

    def GetHeading(self, tm):
        if tm >= self.TR[0] and tm <= self.TR[1]:
            return np.array(self.P)

        return [0,0,0]

    def IsValid(self, t):
        if t >= self.TR[0] and t <= self.TR[1]:
            return True

        return False

class Headings:
    def __init__(self, headings: Heading):
        self.H = headings

    def GetHeading(self, t):
        for h in self.H:
            if h.IsValid(t):
                return h.GetHeading(t)

        return [0,0,0]


class RocketEngine:
    def __init__(self, stages: stage):
        self.stages = stages

    def Burn(self, dt):
        for s in self.stages:
            if s.HasFuel():
                s.Burn(dt)
                break

    def Thrust(self):

        thrust = 0.0
        for s in self.stages:
            if s.HasFuel():
                thrust = s.Thrust()
                break

        return thrust

    def GetMass(self):
        m = 0.0
        for s in self.stages:
            m += s.Fuel()

        return m

class RK4Propagator:
    def __init__(self, llhPos, startTime, dt, engine:RocketEngine, cd, A, headings:Headings, drymass):
        p = pymap3d.geodetic2eci(llhPos[0], llhPos[1], llhPos[2], startTime)
        v = np.cross(OMEGA_E, p)

        st = StateVector(Vec(p[0], p[1],p[2],startTime),Vec(v[0],v[1],v[2], startTime))
        self.InitTime = startTime
        self.State = st
        self.dt = dt
        self.A = A
        self.Cd = cd
        self.engine = engine
        self.headings = headings
        self.drymass = drymass

    def Propagate(self,time):
        tm = self.State.Pos.t
        deltaT = (tm - self.InitTime).seconds
        while tm < time:
            alt = math.sqrt(self.State.Pos.x * self.State.Pos.x + self.State.Pos.y * self.State.Pos.y + self.State.Pos.z * self.State.Pos.z) - 6378000
            if deltaT > 100:
                if alt < 0:
                    break
            pointing = self.headings.GetHeading(tm)
            if pointing[0] == 0 and  pointing[1] == 0 and pointing[2] == 0 :
                pointing = np.array([self.State.Vel.x,self.State.Vel.y,self.State.Vel.z])

            pointing /= np.linalg.norm(pointing)

            mass = self.engine.GetMass() + self.drymass
            thrust = self.engine.Thrust()
            params = [thrust, self.Cd, self.A, pointing, mass]

            self.engine.Burn(self.dt)

            st = self.rk4_step([self.State.Pos.x, self.State.Pos.y, self.State.Pos.z, self.State.Vel.x, self.State.Vel.y, self.State.Vel.z],self.dt, params)
            self.State.Pos.x = st[0]
            self.State.Pos.y = st[1]
            self.State.Pos.z = st[2]
            self.State.Vel.x = st[3]
            self.State.Vel.y = st[4]
            self.State.Vel.z = st[5]
            self.State.Pos.t = tm+datetime.timedelta(seconds=self.dt)
            self.State.Vel.t = tm+datetime.timedelta(seconds=self.dt)
            tm = self.State.Pos.t
            deltaT = (tm - self.InitTime).seconds

        return self.StateInfo()

    def StateInfo(self):
        stP = map.eci2ecef(self.State.Pos.x,self.State.Pos.y,self.State.Pos.z,self.State.Pos.t)
        stV1 = map.eci2ecef(self.State.Pos.x + self.State.Vel.x,self.State.Pos.y + self.State.Vel.y,self.State.Pos.z + self.State.Vel.z,self.State.Pos.t)
        stV = np.array(stV1)-np.array(stP)
        return StateVector(Pos=Vec(stP[0], stP[1], stP[2], self.State.Pos.t), Vel=Vec(stV[0], stV[1], stV[2], self.State.Pos.t))
    # =====================
    # Atmosphere (simple exponential)
    # =====================
    def atmosphere_density(self, r_eci):
        alt = np.linalg.norm(r_eci) - R_E
        if alt < 0:
            return 1.225
        rho0 = 1.225
        H = 8500.0
        return rho0 * np.exp(-alt / H)

    # =====================
    # Gravity (point mass)
    # =====================
    def gravity_accel(self, r):
        r_norm = np.linalg.norm(r)
        return -MU * r / r_norm**3

    # =====================
    # Thrust acceleration
    # =====================
    def thrust_accel(self, thrust, mass, C_bi):
        # Thrust along body +X axis
        F_body = self.engine.Thrust()
        F_eci = C_bi * F_body
        return F_eci / mass

    # =====================
    # Drag acceleration
    # =====================
    def drag_accel(self, r, v, mass, Cd, A):
        rho = self.atmosphere_density(r)
        v_rel = v - np.cross(OMEGA_E, r)
        v_rel_mag = np.linalg.norm(v_rel)

        if v_rel_mag < 1e-3:
            return np.zeros(3)

        return -0.5 * rho * Cd * A * v_rel_mag * v_rel / mass

    # =====================
    # State Derivative
    # =====================
    def derivatives(self, state, params):
        r = np.array(state[0:3])
        v = np.array(state[3:6])

        thrust, Cd, A, pointing, mass = params

        a = self.gravity_accel(r)
        a += self.thrust_accel(thrust, mass, pointing)
        a += self.drag_accel(r, v, mass, Cd, A)

        return np.hstack((v, a))

    # =====================
    # RK4 Integrator
    # =====================
    def rk4_step(self, state, dt, params):
        k1 = self.derivatives(state, params)
        k2 = self.derivatives(state + 0.5 * dt * k1, params)
        k3 = self.derivatives(state + 0.5 * dt * k2, params)
        k4 = self.derivatives(state + dt * k3, params)
        return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


