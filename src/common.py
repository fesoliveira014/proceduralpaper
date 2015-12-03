import numpy as np
from vispy import geometry as mesh

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
	def __init__(self, objId, position = [], geometry = mesh.MeshData()):
		self.id = objId;

		self.position = np.empty(3, dtype=np.float32);
		self.scale = np.empty(3, dtype=np.float32);
		self.geometry = geometry
		self.children = []
		self.isActive = True
		self.isDrawable = True
		
		if(self.id == "window" or self.id == "door" or self.id == "wall"):
			self.texture = self.id
		else:
			self.texture = "no_texture"

	def setPosition(self, position):
		self.position = np.array(position);

	def setScale(self, scale):
		self.scale = np.array(scale);

