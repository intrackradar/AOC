import Types as T
import datetime
Objects = []
StartTime = 0
StopTime = 0
dt = 1
tm = StartTime
ObserverLocation = T.Vec(0,0,0,0)

def Simulate(): 
    results = {}
    for o in Objects:
        results[o]=[]

    tm = StartTime
    while tm < StopTime:

        for o in Objects:
            _ = o.Propagate(tm)
            results[o].append(o.Record(ObserverLocation))

        tm = tm + datetime.timedelta(seconds=dt)
        print("time", tm)

    return results
