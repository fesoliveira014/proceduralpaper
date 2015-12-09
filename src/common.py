import numpy as np

from math import cos, sin, radians

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v/norm

def getYawPitchRollMatrix(yaw, pitch, roll):
    ryaw = radians(yaw)
    rpitch = radians(pitch)
    rroll = radians(roll)

    ca, sa = cos(ryaw), sin(ryaw)
    cb, sb = cos(rpitch), sin(rpitch)
    cc, sc = cos(rroll), sin(rroll)

    rotation = [
        [ca * cc + sa * sb * sc, sc * cb, -sa*cc + ca*sb*sc],
        [-ca*sc + sa*sb*cc, cc*cb, sc*sa + ca*sb*cc],
        [sa*cb, -sb, ca*cb]
    ]

    return np.array(rotation, dtype=np.float32)

class Rule():
    def __init__(self):
        self.name = ""
        self.probability = 1;
        self.parameters = []
        self.childName = []

    def printRule(self):
        print("\tFunction name: " + self.name)
        print("\tFunction paramenters: {", end='')
        for parameter in self.parameters:
            print(parameter + " ", end='')
        print("}")
        print("\tChildren names: {", end='')
        for child in self.childName:
            print(child + " ", end='')
        print("}")
        print("\tProbability: " + str(self.probability))
        print()

class Shape():
    def __init__(self, objId, 
                position = np.empty(3, dtype=np.float32), 
                scale = np.empty(3, dtype=np.float32)):

        self.id = objId;

        self.position = position
        self.scale = scale
        self.children = []
        self.isActive = True
        self.isDrawable = True
        
        if(self.id == "window" or self.id == "door" or self.id == "wall"):
            self.texture = self.id
        else:
            self.texture = "no_texture"

    def setPosition(self, position):
        self.position = np.array(position, np.float32);

    def setScale(self, scale):
        self.scale = np.array(scale, np.float32);

class Mesh():
    def __init__(self, vertex, texture, normal, position = [0,0,0], color = [1,1,1,1]):
        self.position = np.array(position, np.float32)
        self.vertex = np.array(vertex, np.float32)
        self.texture = np.array(texture, np.float32)
        self.normal = np.array(normal, np.float32)
        self.color =  np.array(color, np.float32)

    def buildBuffer(self):
        n = len(self.vertex)
        buf = np.zeros(n, [('a_position', np.float32, 3),
                            ('a_color',   np.float32, 4),
                            ('a_texture',  np.float32, 3),
                            ('a_normal', np.float32, 3)])
        buf['a_position'][:] = self.vertex
        buf['a_color'][:] = self.color
        buf['a_texture'][:] = self.texture
        buf['a_normal'][:] = self.normal

        return buf

class Face():
    def __init__(self, p1, p2, p3):
        self.vertices = [p1, p2, p3]
        self.normal = self.calculateNormal()

    def setVertices(self, p1, p2, p3):
        self.vertices = [p1, p2, p3]
        self.calculateNormal()

    def calculateNormal(self):
        u = self.vertices[1] - self.vertices[0]
        v = self.vertices[2] - self.vertices[0]

        nx = np.dot(u[1], v[2]) - np.dot(u[2], v[1])
        ny = np.dot(u[2], v[0]) - np.dot(u[0], v[2])
        nz = np.dot(u[0], v[1]) - np.dot(u[1], v[0])

        return np.array([nx, ny, nz], dtype = np.float32)

    def containsVertex(self, v):
        for vertex in self.vertices:
            if np.array_equal(v, vertex):
                return True
        return False