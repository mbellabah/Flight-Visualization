"""
Collects serial angle data. That comes in the format "Roll, Pitch, Yaw"
"""


from visual import *
import string, serial, math

import math


def quaternion_to_euler_angle(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z


mySerial = serial.Serial(port='COM10', baudrate=115200, timeout=1)

# Initialize the variables
X = 0
Y = 0
Z = 0


scene = display(title = "Rocket Flight Visualization", width=700, height=700)
scene.up = (0, 0, 1)


class axes():
    def __init__(self):
        arrow(color=color.white, axis=(3, 0, 0), shaftwidth=0.01, fixedwidth=1)
        arrow(color=color.white, axis=(0, 3, 0), shaftwidth=0.01, fixedwidth=1)
        arrow(color=color.white, axis=(0, 0, 3), shaftwidth=0.01, fixedwidth=1)

        label(pos=(1.5, 0, 0), text="Rocket Flight Visualizaton", box=0, opacity=0)
        label(pos=(2, 0, 0), text="X", box=1, opacity=0, color=color.green)
        label(pos=(0, 2, 0), text="Y", box=1, opacity=0, color=color.green)
        label(pos=(0, 0, 2), text="Z", box=1, opacity=0, color=color.green)

class Rocket():
    def __init__(self, pos=(0,0,0), axis=(0,0,.5)):
        scene.select()
        self._pos = vector(pos)
        self._axis = vector(axis)


        # Build the rocket
        self._cone = cone(pos = self._pos, axis = self._axis*.5, radius=0.05, color=color.yellow)
        self._bodytube = cylinder(pos = self._pos, axis=self._axis, radius=0.05, color=color.red)
        self._fin_1 = box(up = (0,0,1), pos = self._pos, axis = self._axis, length=0.01, height=.2, width=.01, color=color.yellow)
        self._fin_2 = box(up=(0, 0, 1), pos=self._pos, axis=self._axis, length=1, height=.2, width=.01,
                          color=color.yellow)

    def rotate_rocket(self, AXIS, UP):
        self._bodytube.axis = AXIS * 0.8
        self._bodytube.up = UP

        self._cone.pos = AXIS * 0.8
        self._cone.axis = AXIS * .3
        self._cone.up = UP

        self._fin_1.pos = AXIS * 0.5
        self._fin_1.axis = AXIS * 0.05
        self._fin_1.up = UP

        self._fin_2.pos = AXIS * 0.05
        self._fin_2.axis = AXIS * 0.05
        self._fin_2.up = UP
        self._fin_2.height = 0.3


coordinateAxes = axes()
myRocket = Rocket()

while True:
    line = mySerial.readline().rstrip()
    sleep(1./120)

    angle_list = string.split(line, ",")

    X, Y, Z = quaternion_to_euler_angle(float(angle_list[0]),float(angle_list[1]), float(angle_list[2]), float(angle_list[3]))

    yaw = deg2rad(X)
    roll = deg2rad(Y)
    pitch = deg2rad(Z)

    axis = vector(cos(pitch) * cos(yaw), -cos(pitch) * sin(yaw), sin(pitch))
    up = vector((sin(roll) * sin(yaw) + cos(roll) * sin(pitch) * cos(yaw),
                 sin(roll) * cos(yaw) - cos(roll) * sin(pitch) * sin(yaw), -cos(roll) * cos(pitch)))


    myRocket.rotate_rocket(axis, up)

    sleep(0.001)

