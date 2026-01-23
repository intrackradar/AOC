import math
import pymap3d as mp
import Types as T
import datetime
import Objects as O
Objects = {}
Observers = {}
StartTime = 0
StopTime = 0
dt = 1
tm = StartTime

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
                rec = Objects[o].RecordFromObserver(Observers[s].State.Pos)

                aer = mp.ecef2aer(results[Objects[o].Name][-1][0],
                                  results[Objects[o].Name][-1][1],
                                  results[Objects[o].Name][-1][2],
                                  Observers[s].Location[0],
                                  Observers[s].Location[1],
                                  Observers[s].Location[2])
                snr = rec[-1][0] - 40*math.log10(aer[2]) + Observers[s].LoopGain
                if snr > Observers[s].SNRLimit and aer[1] > 0.5 and aer[1] < 3.5:
                    Observers[s].Results[Objects[o].Name].append(rec)
                    Observers[s].Results[Objects[o].Name][-1].append(snr)


        tm = tm + datetime.timedelta(seconds=dt)
        print("time", tm)

    return results
