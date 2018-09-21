from visual import *
import string, math, csv


scene = display(title = "Rocket Flight Visualization", width=700, height=700)
scene.up = (1, 0, 0)


class axes():
    def __init__(self):
        arrow(color=color.white, axis=(3, 0, 0), shaftwidth=0.01, fixedwidth=1)
        arrow(color=color.white, axis=(0, 3, 0), shaftwidth=0.01, fixedwidth=1)
        arrow(color=color.white, axis=(0, 0, 3), shaftwidth=0.01, fixedwidth=1)

        label(pos=(1.5, 0, 0), text="Rocket Flight Visualization", box=0, opacity=0)
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

line_list = []
with open('yawPitchRoll.csv') as  csv_file:
    for line in csv_file:
        line_list.append(line.replace('"', ''))


angle_list = string.split(line_list[1], ",")
yaw_deg = float(angle_list[0])
pitch_deg = float(angle_list[1])
roll_deg = float(angle_list[2])


for line in line_list:
    angle_list = string.split(line, ",")

    try:
        roll_deg = float(angle_list[0])
        pitch_deg = float(angle_list[1])
        yaw_deg = float(angle_list[2])
    except:
        continue

    yaw = yaw_deg * 0.0174533
    roll = roll_deg * 0.0174533
    pitch = pitch_deg * 0.0174533

    axis = vector(cos(pitch) * cos(yaw), -cos(pitch) * sin(yaw), sin(pitch))

    up = vector((sin(roll) * sin(yaw) + cos(roll) * sin(pitch) * cos(yaw),
                 sin(roll) * cos(yaw) - cos(roll) * sin(pitch) * sin(yaw), -cos(roll) * cos(pitch)))

    myRocket.rotate_rocket(axis, up)

    sleep(0.001)


