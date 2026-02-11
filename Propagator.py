import datetime

import numpy as np
import math
import Types as T
import pymap3d
import pymap3d as map

# =====================
# Constants
# =====================
MU = 3.986004418e14          # Earth gravitational parameter [m^3/s^2]
R_E = 6378137.0              # Earth radius [m]
OMEGA_E = np.array([0.0, 0.0, 7.2921159e-5])  # Earth rotation [rad/s]
G0 = 9.80665


class Trajectory:
    def __init__(self, times, xs, ys, zs, q0s, q1s, q2s, q3s):
        self.times = times
        self.xs = xs
        self.ys = ys
        self.zs = zs
        self.q0s = q0s
        self.q1s = q1s
        self.q2s = q2s
        self.q3s = q3s

        self.timePoint = times[0]

    def Propagate(self, time):
        self.timePoint = time.timestamp()
        return

    def StateInfo(self):
        st1 = np.array([np.interp(self.timePoint, self.times, self.xs),
               np.interp(self.timePoint, self.times, self.ys),
               np.interp(self.timePoint, self.times, self.zs),
               ])

        qs = np.array([np.interp(self.timePoint, self.times, self.q0s),
                    np.interp(self.timePoint, self.times, self.q1s),
                    np.interp(self.timePoint, self.times, self.q2s),
                    np.interp(self.timePoint, self.times, self.q3s),
               ])
        if self.timePoint < self.times[-1] + 0.01:
            st2 = np.array([np.interp(self.timePoint+0.01, self.times, self.xs),
                            np.interp(self.timePoint+0.01, self.times, self.ys),
                            np.interp(self.timePoint+0.01, self.times, self.zs),
                            ])

            vel = (st2 - st1)*100.0
        else:
            st2 = np.array([np.interp(self.timePoint-0.01, self.times, self.xs),
                            np.interp(self.timePoint-0.01, self.times, self.ys),
                            np.interp(self.timePoint-0.01, self.times, self.zs),
                            ])
            vel = (st1 - st2) * 100.0


        return T.StateVector(Pos=T.Vec(st1[0], st1[1], st1[2], datetime.datetime.fromtimestamp(self.timePoint)), Vel=T.Vec(vel[0], vel[1], vel[2], datetime.datetime.fromtimestamp(self.timePoint)),Qs=qs)


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

        st = T.StateVector(T.Vec(p[0], p[1],p[2],startTime),T.Vec(v[0],v[1],v[2], startTime),[])
        self.InitTime = startTime

        self.State = st
        self.InitAlt = math.sqrt(
            self.State.Pos.x * self.State.Pos.x + self.State.Pos.y * self.State.Pos.y + self.State.Pos.z * self.State.Pos.z)
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
            alt = math.sqrt(self.State.Pos.x * self.State.Pos.x + self.State.Pos.y * self.State.Pos.y + self.State.Pos.z * self.State.Pos.z) - self.InitAlt
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

    # StateInfo should always return ECEF coordinates. NOT ECI!!
    def StateInfo(self):
        stP = map.eci2ecef(self.State.Pos.x,self.State.Pos.y,self.State.Pos.z,self.State.Pos.t)
        stV1 = map.eci2ecef(self.State.Pos.x + self.State.Vel.x*0.01,self.State.Pos.y + self.State.Vel.y*0.01,self.State.Pos.z + self.State.Vel.z*0.01,self.State.Pos.t)
        stV = (np.array(stV1)-np.array(stP))*100
        return T.StateVector(Pos=T.Vec(stP[0], stP[1], stP[2], self.State.Pos.t), Vel=T.Vec(stV[0], stV[1], stV[2], self.State.Pos.t),Qs=[])
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


