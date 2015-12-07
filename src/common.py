import numpy as np
from vispy import geometry as mesh

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v/norm

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
    def __init__(self, vertex, texture, position = [0,0,0], color=[1,1,1,1]):
        self.position = np.array(position, np.float32)
        self.vertex = np.array(vertex, np.float32)
        self.texture = np.array(texture, np.float32)
        self.color = np.array(color, np.float32)

    def buildBuffer(self):
        n = len(self.vertex)
        buf = np.zeros(n, [('a_position', np.float32, 3),
                            ('a_color',   np.float32, 4),
                            ('a_texture',  np.float32, 3)])
        buf['a_position'][:] = self.vertex
        buf['a_color'][:] = self.color
        buf['a_texture'][:] = self.texture

        return buf