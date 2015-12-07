import common
import ruleParser
import numpy as np

from queue import Queue
import random

class ModelBuilder():
    def __init__(self):
        self.tree = common.Shape("start", 
            position = np.array([0,0,0], np.float32), 
            scale = np.array([1.0, 1.0, 1.0], np.float32))
        self.queue = Queue()
        self.queue.put(self.tree)

    def init(self):
        self.tree = common.Shape("start", 
            position = np.array([0,0,0], np.float32), 
            scale = np.array([1.0, 1.0, 1.0], np.float32))
        self.queue = Queue()
        self.queue.put(self.tree)

    def buildModel(self, ruleset):
        random.seed()
        probability = random.random()

        self.init()

        index = 0
        if probability <= 0.4:
            index = 1

        fixedIndex = index

        while not self.queue.empty():
            currentShape = self.queue.get();

            if currentShape.id in ruleset:
                rules = ruleset[currentShape.id]

                if len(rules) <= 1:
                    index = 0

                function = rules[index].name

                if function == "comp":
                    self.comp(rules[index].childName, currentShape)
                elif function == "S":
                    self.s(rules[index].parameters, rules[index].childName, currentShape)
                elif function == "repeat":
                    self.repeat(rules[index].parameters, rules[index].childName, currentShape)
                elif function == "subDiv":
                    self.subDiv(rules[index].parameters, rules[index].childName, currentShape)
                else:
                    self.null(rules[index].childName, currentShape)

            index = fixedIndex



    def null(self, childNames, parent):
        shape = common.Shape(childNames[0], position = parent.position, scale = parent.scale)
        parent.children.append(shape)
        self.queue.put(shape)

    def comp(self, childNames, parent):
        for childName in childNames:
            shape = common.Shape(childName)
            if childName == "front":
                shape.setPosition(parent.position.tolist())
                shape.setScale([parent.scale[0], parent.scale[1], 0])
            
            if childName == "back":
                shape.setPosition([parent.position[0], parent.position[1], parent.position[2] + parent.scale[2]])
                shape.setScale([parent.scale[0], parent.scale[1], 0])

            if childName == "left_facade":
                shape.setPosition(parent.position.tolist())
                shape.setScale([0, parent.scale[1], parent.scale[2]])

            if childName == "right_facade":
                shape.setPosition([parent.position[0] + parent.scale[0], parent.position[1], parent.position[2]])
                shape.setScale([0, parent.scale[1], parent.scale[2]])               
            
            if childName == "top":
                shape.setPosition([parent.position[0], 
                    parent.position[1] + 
                    parent.scale[1], 
                    parent.position[2]])
                shape.setScale([parent.scale[0], 0, parent.scale[2]])

            if childName == "bottom":
                shape.setPosition(parent.position.tolist())
                shape.setScale([parent.scale[0], 0, parent.scale[2]])

            parent.children.append(shape)
            self.queue.put(shape)

    def subDiv(self, parameters, childNames, parent):
        axis = parameters[0]

        parameterIndex = 1

        if axis == '"X"':
            axisPos = parent.position[0]

            for childName in childNames:
                shape = common.Shape(childName)
                shape.setPosition([axisPos, parent.position[1], parent.position[2]])
                shape.setScale([float(parameters[parameterIndex]), parent.scale[1], parent.scale[2]])
                

                axisPos += float(parameters[parameterIndex])
                parameterIndex += 1

                parent.children.append(shape)
                self.queue.put(shape)

        elif axis == '"Y"':
            axisPos = parent.position[1]

            for childName in childNames:
                shape = common.Shape(childName)
                shape.setPosition([parent.position[0], axisPos, parent.position[2]])
                shape.setScale([parent.scale[0], float(parameters[parameterIndex]), parent.scale[2]])

                axisPos += float(parameters[parameterIndex])
                parameterIndex += 1

                parent.children.append(shape)
                self.queue.put(shape)

        elif axis == '"Y"':
            axisPos = parent.position[2]

            for childName in childNames:
                shape = common.Shape(childName)
                shape.setPosition([parent.position[0], parent.position[1]], axisPos)
                shape.setScale([parent.scale[0] , parent.scale[1], float(parameters[parameterIndex])])

                axisPos += parameters[parameterIndex]
                parameterIndex += 1

                parent.children.append(shape)
                self.queue.put(shape)

    def repeat(self, parameters, childNames, parent):
        axis = parameters[0]
        width = int(parameters[1])

        if axis == '"X"':
            childX = parent.position[0]
            repetition = int(parent.scale[0] / width)
            for i in range(0, repetition):
                shape = common.Shape(childNames[0])
                shape.setPosition([childX, parent.position[1], parent.position[2]])
                shape.setScale([width, parent.scale[1], parent.scale[2]])

                childX += width

                parent.children.append(shape)
                self.queue.put(shape)

        else:
            childZ = parent.position[2]
            repetition = int(parent.scale[2] / width)
            for i in range(0, repetition):
                shape = common.Shape(childNames[0])
                shape.setPosition([parent.position[0], parent.position[1], childZ])
                shape.setScale([parent.scale[0], parent.scale[1], width])

                childZ += width

                parent.children.append(shape)
                self.queue.put(shape)

    def s(self, parameters, childNames, parent):
        scale = [float(parameters[0]), float(parameters[1]), float(parameters[2])]
        if len(childNames) == 0:
            parent.setScale(scale)
        else:
            shape = common.Shape(childNames[0])
            shape.setPosition(parent.position.tolist())
            shape.setScale(scale)

            parent.children.append(shape)
            self.queue.put(shape)

    def printTree(self):
        self.queue = Queue()
        self.queue.put(self.tree)

        while not self.queue.empty():
            shape = self.queue.get()
            print("Shape name: " + shape.id) 
            print("  Position: " + str(shape.position.tolist()))
            print("  Scale: " + str(shape.scale.tolist()))
            print("  Children: {")
            for child in shape.children:
                childShape = child
                print("    " + childShape.id)
                self.queue.put(childShape)
            print("  }")
            print("---------------------------------------")


