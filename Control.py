import Simulator as S
import numpy as np
import pymap3d as map
import Types as T
import Propagator as P
import math
import importlib
import matplotlib
import pandas as pd
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import Objects as O
import ObjectData as OD
import Helper as H
importlib.reload(H)
importlib.reload(O)
importlib.reload(OD)
importlib.reload(plt)
importlib.reload(T)
importlib.reload(S)
importlib.reload(P)
import pyvista as pv
import vtk
from PIL import Image
import datetime





# Define initial simulation start time
startTime = datetime.datetime(2025,1,1,1,1,1,1)

# load in all the objects
# for o in OD.objects:
#     S.Objects[o] = O.LoadObject(OD.objects[o])
#     break
S.Objects["pencil"] = O.LoadObject(OD.objects["pencil"])
S.Objects["almond"] = O.LoadObject(OD.objects["almond"])
S.Objects["tcone"] = O.LoadObject(OD.objects["tcone"])

# S.Objects["pencil"] = O.LoadObject("pencil")
# load in all the sensors / observers
for s in OD.sensors:
    S.Observers[s] = O.LoadObserver(OD.sensors[s])

# Set the simulation start time and stop times
datetime.datetime.fromisoformat(OD.simulation["start time"])
S.StartTime = datetime.datetime.fromisoformat(OD.simulation["start time"])
S.StopTime = datetime.datetime.fromisoformat(OD.simulation["stop time"])
S.dt = OD.simulation["time step"]

# Run the simulation
res = S.Simulate()

# Separate the output for each object from the simulation results object
output = []
for o in res:
    output.append(res[o])

# The rest of these are graphs
# TODO: Add graphs filtered based on each site's visibility
#  Clean up graphs to handle multiple sites.

#
# globe plot trajectory
texture = pv.read_texture("C:\\Users\\Jerem\\Downloads\\world.topo.bathy.200412.3x21600x10800.jpg")
radius = 6371000.0  # km (any scale works)

sphere = pv.Sphere(radius=radius, theta_resolution=360, phi_resolution=180)

pts = sphere.points
x1, y1, z1 = pts[:, 0], pts[:, 1], pts[:, 2]

# Convert XYZ to spherical angles
theta = np.arctan2(y1, x1)        # longitude angle
phi = np.arcsin(z1 / radius)     # latitude angle

# Normalize to [0, 1] for UV texture
u = (theta + np.pi) / (2 * np.pi)       # 0 → 1
v = (phi + np.pi/2) / np.pi             # 0 → 1

uv = np.column_stack([u, v])

# Attach UV coords to the mesh
uv_vtk = vtk.vtkFloatArray()
uv_vtk.SetNumberOfComponents(2)
uv_vtk.SetNumberOfTuples(len(uv))
uv_vtk.SetName("TextureCoordinates")
for i in range(len(uv)):
    uv_vtk.SetTuple(i, uv[i])

sphere.GetPointData().SetTCoords(uv_vtk)

plotter = pv.Plotter()
plotter.add_mesh(sphere, texture=texture)
# Add the LLH points
counter = 0
colors = ["black","orange","grey"]
for s in S.Observers:
    x,y,z,vx,vy,vz,t = H.ConvertResToVecs(S.Observers[s].Results["pencil"])
    if len(x) == 0:
        continue
    points = np.column_stack((x,y,z))
    plotter.add_points(points, color=colors[counter], point_size=25,label=s)
    counter+=1

# Add the LLH points
x,y,z,vx,vy,vz,t = H.ConvertResToVecs(output[0])

points = np.column_stack((x,y,z))
plotter.add_points(points, color="red", point_size=10)
plotter.add_legend()



# points = np.column_stack((ObsLoc[0],ObsLoc[1],ObsLoc[2]))
# plotter.add_points(points, color="Orange", point_size=10)
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[1])
#
# points = np.column_stack((x,y,z))
# plotter.add_points(points, color="black", point_size=10)

plotter.add_axes()
plotter.show()





#
# ## Range versus RCS
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[ii])
#
#     rng = []
#     for ii in range(len(x)):
#         rng.append(np.linalg.norm([x[ii]-ObsLoc[0],y[ii]-ObsLoc[1],z[ii]-ObsLoc[2]]))
#
#     p,=ax.plot(np.array(rng)/1000,r)
#     ps.append(p)
#
# ax.legend(ps,names)
#
# ax.set_xlabel("Range (km)")
# ax.set_ylabel("RCS")
# ax.grid()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[ii])
#
#     rng = []
#     for ii in range(len(x)):
#         rng.append(np.linalg.norm([x[ii]-ObsLoc[0],y[ii]-ObsLoc[1],z[ii]-ObsLoc[2]]))
#
#     p,=ax.plot(az,r)
#     ps.append(p)
#
# ax.legend(ps,names)
#
# ax.set_xlabel("Incident Az (Deg)")
# ax.set_ylabel("RCS")
# ax.grid()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[ii])
#
#     rng = []
#     for ii in range(len(x)):
#         rng.append(np.linalg.norm([x[ii]-ObsLoc[0],y[ii]-ObsLoc[1],z[ii]-ObsLoc[2]]))
#
#     p,=ax.plot(el,r)
#     ps.append(p)
#
# ax.legend(ps,names)
# ax.set_xlabel("Incident El (Deg)")
# ax.set_ylabel("RCS")
# ax.grid()
#
# ## Az-El-RCS graph
# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
#
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[ii])
#
#     p,=ax.plot(az,el,r)
#     ps.append(p)
#
# ax.legend(ps,names)
#
# ax.set_zlabel("RCS (dBsm)")
# ax.set_xlabel("Az (deg)")
# ax.set_ylabel("El (deg)")
#
# ## Time-Distance-RCS graph
# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
#
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,rcs, az, el = ConvertResToVecs(output[ii])
#
#     rng = []
#     for ii in range(len(x)):
#         rng.append(np.linalg.norm([x[ii]-ObsLoc[0],y[ii]-ObsLoc[1],z[ii]-ObsLoc[2]]))
#
#     p,=ax.plot([tm.seconds for tm in (t-startTime)],np.array(rng)/1000,rcs)
#     ps.append(p)
#
# ax.legend(ps,names)
#
# ax.set_zlabel("RCS (dBsm)")
# ax.set_xlabel("Time (Sec)")
# ax.set_ylabel("Range (km)")
#
# ## Time-Altitude-RCS graph
# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
#
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,rcs, az, el = ConvertResToVecs(output[ii])
#
#     rng = []
#     for ii in range(len(x)):
#         rng.append(np.linalg.norm([x[ii]-ObsLoc[0],y[ii]-ObsLoc[1],z[ii]-ObsLoc[2]]))
#     llh = map.ecef2geodetic(x,y,z)
#     p,=ax.plot([tm.seconds for tm in (t-startTime)],llh[2]/1000,rcs)
#     ps.append(p)
#
# ax.legend(ps,names)
#
# ax.set_zlabel("RCS (dBsm)")
# ax.set_xlabel("Time (Sec)")
# ax.set_ylabel("Altitude (km)")
# plt.show()
#
# ## Time versus RCS
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# ps = []
# for ii in range(len(data)):
#     x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[ii])
#
#     rng = []
#     for ii in range(len(x)):
#         rng.append(np.linalg.norm([x[ii]-ObsLoc[0],y[ii]-ObsLoc[1],z[ii]-ObsLoc[2]]))
#
#     p,=ax.plot([tm.seconds for tm in (t-startTime)],r)
#     ps.append(p)
#
# ax.legend(ps,names)
#
# ax.set_xlabel("Time (s)")
# ax.set_ylabel("RCS (dBsm)")
# ax.grid()
#
# ## 3d matplot lib plot of trajectory colored by RCS
# fig = plt.figure(figsize=(18, 6))
# ax1 = fig.add_subplot(131,projection='3d')
# ax2 = fig.add_subplot(132, projection='3d')
# ax3 = fig.add_subplot(133, projection='3d')
#
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[0])
#
# p1=ax1.scatter(x/1000,y/1000,z/1000, c = r, cmap = "jet")
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[1])
#
# p2=ax2.scatter(x/1000,y/1000,z/1000, c = r, cmap = "jet")
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[2])
#
# p3=ax3.scatter(x/1000,y/1000,z/1000, c = r, cmap = "jet")
#
#
# ax1.set_zlabel("Z")
# ax1.set_xlabel("X")
# ax1.set_ylabel("Y")
# ax1.set_title("Almond 40")
# ax2.set_zlabel("Z")
# ax2.set_xlabel("X")
# ax2.set_ylabel("Y")
# ax2.set_title("Pencil 100")
# ax3.set_zlabel("Z")
# ax3.set_xlabel("X")
# ax3.set_ylabel("Y")
# ax3.set_title("Cone")
# cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
# cbar1.set_label("RCS (dBsm)")
# cbar2 = fig.colorbar(p2, ax=ax2, shrink=0.7)
# cbar2.set_label("RCS (dBsm)")
# cbar3 = fig.colorbar(p3, ax=ax3, shrink=0.7)
# cbar3.set_label("RCS (dBsm)")
# # plt.show()
#
# ## 3d matplot lib plot of trajectory colored by RCS
# fig = plt.figure(figsize=(18, 6))
# ax1 = fig.add_subplot(131,projection='3d')
# ax2 = fig.add_subplot(132, projection='3d')
# ax3 = fig.add_subplot(133, projection='3d')
#
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[0])
# llh = map.ecef2geodetic(x,y,z)
# p1=ax1.scatter(llh[1] % 360, llh[0],llh[2]/1000, c = r, cmap = "jet")
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[1])
# llh = map.ecef2geodetic(x,y,z)
# p2=ax2.scatter(llh[1] % 360, llh[0],llh[2]/1000, c = r, cmap = "jet")
#
# x,y,z,vx,vy,vz,t,r, az, el = ConvertResToVecs(output[2])
# llh = map.ecef2geodetic(x,y,z)
# p3=ax3.scatter(llh[1] % 360, llh[0],llh[2]/1000, c = r, cmap = "jet")
#
#
# ax1.set_zlabel("Alt (km)")
# ax1.set_xlabel("Lon (deg)")
# ax1.set_ylabel("Lat (deg)")
# ax1.set_title("Almond 40")
# ax2.set_zlabel("Alt (km)")
# ax2.set_xlabel("Lon (deg)")
# ax2.set_ylabel("Lat (deg)")
# ax2.set_title("Pencil 100")
# ax3.set_zlabel("Alt (km)")
# ax3.set_xlabel("Lon (deg)")
# ax3.set_ylabel("Lat (deg)")
# ax3.set_title("Cone")
# cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
# cbar1.set_label("RCS (dBsm)")
# cbar2 = fig.colorbar(p2, ax=ax2, shrink=0.7)
# cbar2.set_label("RCS (dBsm)")
# cbar3 = fig.colorbar(p3, ax=ax3, shrink=0.7)
# cbar3.set_label("RCS (dBsm)")
#
# plt.show()

## 3d matplot lib plot of trajectory colored by RCS
fig = plt.figure(figsize=(18, 6))
ax1 = fig.add_subplot(111,projection='3d')
labels = []
ps = []
for s in S.Observers:
    x,y,z,vx,vy,vz,t, rcs, az, el = H.ConvertResToVecs2(S.Observers[s].Results["pencil"])
    if len(x) == 0:
        continue
    llh = map.ecef2geodetic(x, y, z)
    p1 = ax1.scatter(llh[1] % 360, llh[0], llh[2] / 1000, cmap="jet")
    ps.append(p1)
    labels.append(s)
    counter+=1

ax1.set_zlabel("Alt (km)")
ax1.set_xlabel("Lon (deg)")
ax1.set_ylabel("Lat (deg)")
ax1.legend(ps,labels)
# cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
# cbar1.set_label("RCS (dBsm)")
plt.show()

## 3d matplot lib plot of trajectory colored by RCS
fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(111,projection='3d')
labels = []
ps = []
for s in S.Observers:
    x,y,z,vx,vy,vz,t, rcs, az, el = H.ConvertResToVecs2(S.Observers[s].Results["pencil"])
    if len(x) == 0:
        continue
    llh = map.ecef2geodetic(x, y, z)
    p1 = ax1.scatter(xs=[tm.timestamp() for tm in t], ys=llh[2] / 1000, zs=rcs)
    ps.append(p1)
    labels.append(s)
    counter+=1

ax1.set_xlabel("Time")
ax1.set_ylabel("Alt (km)")
ax1.set_zlabel("RCS (dBsm")
ax1.legend(ps,labels)
# cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
# cbar1.set_label("RCS (dBsm)")
plt.show()


fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(111)
labels = []
ps = []
shapes = ["+","*"]
counter = 0
for s in S.Observers:
    x,y,z,vx,vy,vz,t, rcs, az, el = H.ConvertResToVecs2(S.Observers[s].Results["pencil"])
    if len(x) == 0:
        continue
    llh = map.ecef2geodetic(x, y, z)
    p1 = ax1.scatter(x=[tm.timestamp() for tm in t], y=rcs, c=llh[2] / 1000, cmap="jet",marker = shapes[counter])
    ps.append(p1)
    labels.append(s)
    counter+=1

ax1.set_xlabel("Time")
ax1.set_ylabel("RCS (dBsm")
ax1.legend(ps,labels)
cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
cbar1.set_label("Altitude (km)")
ax1.grid()
plt.show()

fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(111)
labels = []
ps = []
shapes = ["+","*"]
counter = 0
for s in S.Observers:
    x,y,z,vx,vy,vz,t, rcs, az, el = H.ConvertResToVecs2(S.Observers[s].Results["pencil"])
    if len(x) == 0:
        continue
    aer = map.ecef2aer(x, y, z, S.Observers[s].Location[0],S.Observers[s].Location[1],S.Observers[s].Location[2])
    p1 = ax1.scatter(x=aer[2]*0.001, y=rcs, cmap="jet",marker = shapes[counter])
    ps.append(p1)
    labels.append(s)
    counter+=1

ax1.set_xlabel("Range (km)")
ax1.set_ylabel("RCS (dBsm")
ax1.legend(ps,labels)
# cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
# cbar1.set_label("Altitude (km)")
ax1.grid()
plt.show()

fig = plt.figure(figsize=(18, 6))
ax1 = fig.add_subplot(131,projection='3d')
ax2 = fig.add_subplot(132, projection='3d')
ax3 = fig.add_subplot(133, projection='3d')
shapes = ["+","*","--"]
counter = 0
p1label = []
p1s = []
for s in S.Observers:
    x,y,z,vx,vy,vz,t,r, az, el = H.ConvertResToVecs2(S.Observers[s].Results["almond"])
    if len(x) == 0:
        continue
    llh = map.ecef2geodetic(x,y,z)
    p1=ax1.scatter(llh[1] % 360, llh[0],llh[2]/1000, c = r, cmap = "jet",marker=shapes[counter])
    p1s.append(p1)
    p1label.append(s)
    counter+=1
counter = 0
p2label = []
p2s = []
for s in S.Observers:
    x,y,z,vx,vy,vz,t,r, az, el = H.ConvertResToVecs2(S.Observers[s].Results["pencil"])
    if len(x) == 0:
        continue
    llh = map.ecef2geodetic(x,y,z)
    p2=ax2.scatter(llh[1] % 360, llh[0],llh[2]/1000, c = r, cmap = "jet",marker=shapes[counter])
    p2s.append(p2)
    p2label.append(s)
    counter+=1
counter = 0
p3label = []
p3s = []
for s in S.Observers:
    x,y,z,vx,vy,vz,t,r, az, el = H.ConvertResToVecs2(S.Observers[s].Results["tcone"])
    if len(x) == 0:
        continue
    llh = map.ecef2geodetic(x,y,z)
    p3=ax3.scatter(llh[1] % 360, llh[0],llh[2]/1000, c = r, cmap = "jet",marker=shapes[counter])
    p3s.append(p3)
    p3label.append(s)
    counter+=1


ax1.set_zlabel("Alt (km)")
ax1.set_xlabel("Lon (deg)")
ax1.set_ylabel("Lat (deg)")
ax1.set_title("Almond")
ax1.legend(p1s,p1label)
ax2.set_zlabel("Alt (km)")
ax2.set_xlabel("Lon (deg)")
ax2.set_ylabel("Lat (deg)")
ax2.set_title("Pencil")
ax2.legend(p2s,p2label)
ax3.set_zlabel("Alt (km)")
ax3.set_xlabel("Lon (deg)")
ax3.set_ylabel("Lat (deg)")
ax3.set_title("Truncated Cone")
ax3.legend(p3s,p3label)
cbar1 = fig.colorbar(p1, ax=ax1, shrink=0.7)
cbar1.set_label("RCS (dBsm)")
cbar2 = fig.colorbar(p2, ax=ax2, shrink=0.7)
cbar2.set_label("RCS (dBsm)")
cbar3 = fig.colorbar(p3, ax=ax3, shrink=0.7)
cbar3.set_label("RCS (dBsm)")

plt.show()


# xp = math.sin(190/57.295)
# yp = math.cos(190/57.295)
# xleft = math.sin(350/57.295)
# yleft=math.cos(350/57.295)
# xright = math.sin(345/57.295)
# yright = math.cos(345/57.295)
#
# si = xright*yleft-yright*xleft
# co = xright*xleft + yleft*yright
#
# si = xright*yleft-yright*xleft
# co = xright*xleft + yleft*yright
#
# math.atan2(si,co)*57.295 % 360