import numpy as np
import math

def WriteTrajectory(states, filename):
    with open(filename,"w") as fi:
        fi.write("Time (s),X (m),Y (m),Z (m),q1 (norm),q2 (i),q3 (j),q4 (k)\n")

        for s in states:
            fi.write(f"{s[0].timestamp()}, {s[1]}, {s[2]}, {s[3]}, {s[7]}, {s[8]},{s[9]},{s[10]}\n")

def ConvertQs2UnitVecs(q0, q1, q2, q3):

    return np.array([1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)]), \
            np.array([2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q0 * q1)]),\
            np.array([2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 * q1 + q2 * q2)])

def ConvertUnitVecs2Qs(xUnit,yUnit, zUnit):
    trace = xUnit[0] + yUnit[1] + zUnit[2]
    q0 = 0
    q1 = 0
    q2 = 0
    q3 = 0
    if trace <= 0:
        # print("trace < 0", trace)
        if xUnit[0] > yUnit[1] and xUnit[0] > zUnit[2]:
            s = 2 * math.sqrt(1 + xUnit[0] - yUnit[1] - zUnit[2])
            q0 = (zUnit[1] - yUnit[2]) / s
            q1 = 0.25 * s
            q2 = (xUnit[1] + yUnit[0]) / s
            q3 = (xUnit[2] + zUnit[0]) / s

        if yUnit[1] > xUnit[0] and yUnit[1] > zUnit[2]:
            s = 2 * math.sqrt(1 - xUnit[0] + yUnit[1] - zUnit[2])
            q0 = (xUnit[2] - zUnit[0]) / s
            q1 = (xUnit[1] + yUnit[0]) / s
            q2 = 0.25 * s
            q3 = (yUnit[2] + zUnit[1]) / s

        if zUnit[2] > yUnit[1] and zUnit[2] > xUnit[0]:
            s = 2 * math.sqrt(1 - xUnit[0] - yUnit[1] + zUnit[2])
            q0 = (yUnit[0] - xUnit[1]) / s
            q1 = (xUnit[2] + zUnit[0]) / s
            q2 = (yUnit[2] + zUnit[1]) / s
            q3 = 0.25 * s

    if trace > 0:
        s = 2 * math.sqrt(trace + 1)
        q0 = 0.25 * s
        q1 = (zUnit[1] - yUnit[2]) / s
        q2 = (xUnit[2] - zUnit[0]) / s
        q3 = (yUnit[0] - xUnit[1]) / s

    return q0, q1, q2, q3

# ConvertRestToVecs is a helper function that converts the simulation results for an object into individual traces for plotting
def ConvertResToVecs(res):
    x = []
    y = []
    z = []
    vx = []
    vy = []
    vz = []
    t = []


    for r in res:
        x.append(r[0])
        y.append(r[1])
        z.append(r[2])
        vx.append(r[3])
        vy.append(r[4])
        vz.append(r[5])
        t.append(r[6])

    return np.array(x), np.array(y), np.array(z), np.array(vx), np.array(vy), np.array(vz), np.array(t)


# ConvertRestToVecs is a helper function that converts the simulation results for an object into individual traces for plotting
def ConvertResToVecs2(res):
    x = []
    y = []
    z = []
    vx = []
    vy = []
    vz = []
    t = []
    rcs = []
    az = []
    el = []
    snr = []

    for r in res:
        x.append(r[0])
        y.append(r[1])
        z.append(r[2])
        vx.append(r[3])
        vy.append(r[4])
        vz.append(r[5])
        t.append(r[6])
        rcs.append(r[7][0])
        az.append(r[7][1])
        el.append(r[7][2])
        snr.append(r[8])

    return np.array(x), np.array(y), np.array(z), np.array(vx), np.array(vy), np.array(vz), np.array(t), np.array(rcs), np.array(az), np.array(el), np.array(snr)