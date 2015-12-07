import numpy as np
from vispy.util.transforms import perspective, translate, rotate

from enum import Enum

import common

class MoveDirection(Enum):
    forward = 1
    back = 2
    left = 3
    right = 4
    up = 5
    down = 6

class CameraState(Enum):
    still = 1
    pan = 2

class CameraMoveState():
    def __init__(self):
        self.forward = False
        self.back = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False

class Camera():
    def __init__(self, position, lookat, fov, viewport):
        self.position = position
        self.fov = fov
        self.width, self.height = viewport

        self.position = position
        self.lookat = lookat

        self.speed = 0.5
        self.aspect = self.width / self.height

        self.moveStates = CameraMoveState()

        self.target = np.dot(self.position, self.lookat)
        self.up = np.array([0, 1, 0])
        self.right = np.cross(self.up, self.lookat)

        self.view = self.setView(self.position, self.target, self.up)
        self.msec = 1

        self.translation = np.zeros(3, np.float32)

    def setView(self, eye, target, up):
        zaxis = common.normalize(eye - target)
        xaxis = common.normalize(np.cross(up, zaxis))
        yaxis = np.cross(zaxis, xaxis)

        xlist = xaxis.tolist()
        ylist = yaxis.tolist()
        zlist = zaxis.tolist()

        xlist.append(-np.dot(xaxis, eye))
        ylist.append(-np.dot(yaxis, eye))
        zlist.append(-np.dot(zaxis, eye))

        orientation = np.array([xlist, ylist, zlist, [0,0,0,1]])

        return np.transpose(orientation)

    def update(self, msec = 1):
        self.msec = msec
        self.move3D()

        self.position += self.translation
        # print('translation: ' + str(self.translation))
        
        self.translation = np.zeros(3, np.float32)

        # print('position: ' + str(self.position))

        self.lookat = np.dot(np.eye(3, dtype=np.float32), np.array([0,0,1]))
        self.target = self.position + self.lookat

        self.up = np.dot(np.eye(3, dtype=np.float32), np.array([0,1,0]))
        self.right = np.cross(self.up, self.lookat)

        self.view = self.setView(self.position, self.target, self.up)
        # print(str(self.view))

    def move3D(self):
        if self.moveStates.forward == True:
            self.walk(self.speed * self.msec)

        if self.moveStates.back == True:
            self.walk(-self.speed * self.msec)

        if self.moveStates.left == True:
            self.strife(self.speed * self.msec)

        if self.moveStates.right == True:
            self.strife(-self.speed * self.msec)

        if self.moveStates.up == True:
            self.lift(self.speed * self.msec)

        if self.moveStates.down == True:
            self.lift(-self.speed * self.msec)

    def walk(self, distance):
        self.translation += self.lookat * distance

    def strife(self, distance):
        self.translation += self.right * distance

    def lift(self, distance):
        self.translation += self.up * distance

    def onKeyPress(self, event):
        if event.text == 'w':
            print("w")
            self.moveStates.forward = True

        if event.text == 's':
            print("s")
            self.moveStates.back = True

        if event.text == 'd':
            print("d")
            self.moveStates.right = True
           
        if event.text == 'a':
            print("a")
            self.moveStates.left = True

        if event.text == ' ':
            self.moveStates.up = True

        if event.text == 'c':
            self.moveStates.down = True


    def onKeyRelease(self, event):
        if event.text == 'w':
            self.moveStates.forward = False

        if event.text == 's':
            self.moveStates.back = False

        if event.text == 'd':
            self.moveStates.right = False

        if event.text == 'a':
            self.moveStates.left = False

        if event.text == ' ':
            self.moveStates.up = False

        if event.text == 'c':
            self.moveStates.down = False





