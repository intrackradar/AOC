import math
import pymap3d as mp
import Types as T
import datetime
import Objects as O
import numpy as np
Objects = {}
Observers = {}
StartTime = 0
StopTime = 0
dt = 1
tm = StartTime

Deg2Rad = math.pi/180.0


def Simulate(): 
    results = {}
    for o in Objects:
        results[Objects[o].Name]=[]
    for s in Observers:
        Observers[s].Results = {}
        for o in Objects:
            Observers[s].Results[Objects[o].Name] = []
    tm = StartTime

    while tm < StopTime:

        for o in Objects:
            _ = Objects[o].Propagate(tm)
            results[Objects[o].Name].append(Objects[o].Record())
            for s in Observers:
                # print(results[Objects[o].Name])




                # numerical derivative of positions for velocity calculation, because PyMap3d doesn't support velocity conversions and I'm lazy...
                # using dt of 0.01 seconds
                enu = mp.ecef2enu(results[Objects[o].Name][-1][0],
                                 results[Objects[o].Name][-1][1],
                                 results[Objects[o].Name][-1][2],
                                 Observers[s].Location[0],
                                 Observers[s].Location[1],
                                 Observers[s].Location[2])

                aer = mp.enu2aer(enu[0],enu[1],enu[2])

                v1 = mp.ecef2enu(results[Objects[o].Name][-1][0] + results[Objects[o].Name][-1][3]*0.01,
                                  results[Objects[o].Name][-1][1] + results[Objects[o].Name][-1][4]*0.01,
                                  results[Objects[o].Name][-1][2] + results[Objects[o].Name][-1][5]*0.01,
                                  Observers[s].Location[0],
                                  Observers[s].Location[1],
                                  Observers[s].Location[2])
                vel = [0,0,0]
                vel[0] = (v1[0] - enu[0]) / 0.01
                vel[1] = (v1[1] - enu[1]) / 0.01
                vel[2] = (v1[2] - enu[2]) / 0.01

                mag=np.linalg.norm(enu)

                # range unit vector dot with velocity vector for range rate
                Freq = Observers[s].Frequency+2*(enu[0]*vel[0]+enu[1]*vel[1]+enu[2]*vel[2])*Observers[s].Frequency/(3.0e8*mag)
                rec = Objects[o].RecordFromObserver(Observers[s].State.Pos, Freq)

                yp = math.cos(aer[0] * Deg2Rad)
                xp = math.sin(aer[0] * Deg2Rad)

                xleft = Observers[s].AzFence[0][0]
                yleft = Observers[s].AzFence[0][1]

                si = xp * yleft - yp * xleft
                co = xp * xleft + yleft * yp

                ang = math.atan2(si,co) % (2*math.pi)
                elEr = Observers[s].Fence[1] - aer[1]
                beamloss = math.exp(-0.5 * 1.3862943611198906 * elEr*elEr/(Observers[s].Beamwidth*Observers[s].Beamwidth))
                # ang <= Observers[s].AzFence[1] and \
                # (aer[1] >= Observers[s].Fence[1][0]) and
                # if beamloss > 0:
                if aer[1] > 0.0 and beamloss > 0:
                    snr = rec[-1][0] - 40*math.log10(aer[2]) + Observers[s].LoopGain + 10*math.log10(beamloss)
                    if snr > Observers[s].SNRLimit:
                        Observers[s].Results[Objects[o].Name].append(rec)
                        Observers[s].Results[Objects[o].Name][-1].append(snr)


        tm = tm + datetime.timedelta(seconds=dt)
        print("time", tm)

    return results
