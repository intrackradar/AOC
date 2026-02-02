import numpy as np

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