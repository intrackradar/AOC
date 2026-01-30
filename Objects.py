import datetime
import math

import pandas as pd
import Propagator
import Propagator as P
import ObjectData as OD
import Types as T
import numpy as np
import pymap3d as mp
Objects = {}
ObjectJSON = OD.objects

Deg2Rad = math.pi/180.0

class ParsedJSONObserver:
    def __init__(self, jsonData):
        self.Name = jsonData["name"]
        self.Location = [jsonData["location"]["lat"], jsonData["location"]["lon"],
                               jsonData["location"]["heightM"]]

        xleft = math.sin(jsonData["fence"]["az"][0] * Deg2Rad)
        yleft = math.cos(jsonData["fence"]["az"][0] * Deg2Rad)
        xright = math.sin(jsonData["fence"]["az"][1] * Deg2Rad)
        yright = math.cos(jsonData["fence"]["az"][1] * Deg2Rad)

        si = xright * yleft - yright * xleft
        co = xright * xleft + yleft * yright

        self.AzFence = [[xleft, yleft],math.atan2(si,co) % (2*math.pi)]
        self.Fence = [jsonData["fence"]["az"],jsonData["fence"]["el"]]
        self.Beamwidth = jsonData["beamwidth"]
        self.LoopGain = jsonData["loopgain"]
        self.Frequency = jsonData["frequency"]
        self.Results = {}
        ecef = mp.geodetic2ecef(self.Location[0],self.Location[1],self.Location[2])
        self.State = T.StateVector(Pos = T.Vec(x=ecef[0],y=ecef[1], z=ecef[2],t=datetime.datetime(year=2025,month=1,day=1)), Vel = T.Vec(0,0,0,datetime.datetime(year=2025,month=1,day=1)))
        self.SNRLimit = jsonData["snrlimit"]


class ParsedJSONObject:
    def __init__(self, jsonData):

        # parse rocket stages
        Stages = []
        st = 1
        while True:

            try:
                stageData = jsonData["RocketStages"][f"stage {st:1d}"]
                st += 1
                tempS = P.stage(stageData["fuel mass"], stageData["thrust"],stageData["isp"])
                Stages.append(tempS)
            except:
                break

        RE = P.RocketEngine(Stages)
        self.rocketEngine = RE

        self.LaunchLocation = [jsonData["Launch Location"]["lat"], jsonData["Launch Location"]["lon"], jsonData["Launch Location"]["heightM"]]
        self.LaunchTime = datetime.datetime.fromisoformat(jsonData["Launch Time"])

        # parse headings
        Headings = []
        st = 1

        while True:

            try:
                headingData = jsonData["Headings"]["Heading "+str(st)]
                st += 1
                az = headingData["Pointing"][0]
                el = headingData["Pointing"][1]
                baseLoc = np.array(mp.geodetic2eci(self.LaunchLocation[0], self.LaunchLocation[1], self.LaunchLocation[2], self.LaunchTime))
                pointings = np.array(mp.aer2eci(az, el, 1.0, self.LaunchLocation[0], self.LaunchLocation[1], self.LaunchLocation[2], self.LaunchTime)) - baseLoc
                tempH = P.Heading([datetime.datetime.fromisoformat(headingData["Time Range"][0]),datetime.datetime.fromisoformat(headingData["Time Range"][1])],pointings)
                Headings.append(tempH)
            except:
                break
        self.Headings = P.Headings(Headings)
        print(Headings)
        self.Propagator = P.RK4Propagator(self.LaunchLocation,self.LaunchTime,jsonData["Propagator Time Step"],RE,jsonData["Aerodynamics"]["Cd"],jsonData["Aerodynamics"]["A"],self.Headings,jsonData["Drymass"])

        rcsDataSets = []
        rcsFreqs = []
        for f in jsonData["RCSData"]:
            data = pd.read_excel(jsonData["RCSData"][f]["url"], sheet_name=jsonData["RCSData"][f]["sheetname"])
            rmap = {}
            # print(data)
            for ii in range(data.shape[0]):

                vals = data.loc[ii]
                # print(vals)
                try:
                    e = vals[1]
                    a = vals[2]
                    r1 = vals[3]
                    try:
                        e = float(e)
                        a = float(a)
                        r1 = float(r1)
                    except:
                        # print(e, a, r1, math.isnan(e))
                        continue
                    if math.isnan(e):
                        # print(e, a, r1, math.isnan(e))
                        continue

                    if a in rmap:
                        rmap[a][e] = r1
                    else:
                        rmap[a] = {}
                        rmap[a][e] = r1
                except:
                    continue
            # print(rmap)
            precision = np.round(np.mean(np.diff(np.array(list(rmap.keys()))) % 360), 1)
            rcsMap1 = T.RCSMapAzEl(rmap, precision, 180)
            rcsDataSets.append(rcsMap1)
            rcsFreqs.append(jsonData["RCSData"][f]["frequency"])

        rcsFreqs = np.array(rcsFreqs)
        rcsDataSets = np.array(rcsDataSets)
        inds = np.argsort(rcsFreqs)
        rcsFreqs = rcsFreqs[inds]
        rcsDataSets = rcsDataSets[inds]
        self.RCSData = T.RCSMap(rcsDataSets, rcsFreqs)
        self.Name = jsonData["name"]
        self.Obj = T.Obj(self.Name,self.RCSData,self.Propagator)


def LoadObject(data):
    return ParsedJSONObject(data).Obj

def LoadObserver(data):
    return ParsedJSONObserver(data)