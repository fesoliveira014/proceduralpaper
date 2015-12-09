import numpy as np

import common
import meshBuilder

class MeshBuilder():
	def __init__(self):
		self.vertexBuffer = []
		self.textureBuffer = []
		self.normalBuffer = []
		self.faces = []
		self.queue = []
		self.shapeList = []
		self.isTraversalOver = False

	def buildMeshFromTree(self, tree):
		self.queue.append(tree)
		self.buildShapeList()
		self.buildVertexBuffer()
		print('number of vertices: ' + str(len(self.vertexBuffer)))
		print('number of faces: ' + str(len(self.faces)))
		self.buildNormalsFromFaces()
		print('number of normals: ' + str(len(self.normalBuffer)))


	def buildShapeList(self):
		while not self.isTraversalOver:
			self.isTraversalOver = True
			self.shapeList = []
			tempQueue = []

			for shape in self.queue:
				self.shapeList.append(shape)

				if len(shape.children) > 0:
					self.isTraversalOver = False

					for child in shape.children:
						tempQueue.append(child)
				else: 
					tempQueue.append(shape)

			self.queue = tempQueue

	def buildVertexBuffer(self):
		for shape in self.shapeList:
			self.buildVertexListFromShape(shape)


	def buildVertexListFromShape(self, shape):
		index = 0.0
		if shape.texture == "window":
			index = 1.0
		elif shape.texture == "door":
			index = 2.0
		elif shape.texture == "wall":
			index = 3.0

		if shape.scale[0] > 0 and shape.scale[1] > 0 and shape.scale[2] > 0:
			self.buildVertexFromCoords(shape.position, shape.scale, [True, True, False], index)
			self.buildVertexFromCoords(shape.position, shape.scale, [True, False, True], index)
			self.buildVertexFromCoords(shape.position, shape.scale, [False, True, True], index)

			posX = shape.position
			posY = shape.position
			posZ = shape.position

			posX[0] += shape.scale[0]
			posY[1] += shape.scale[1]
			posZ[2] += shape.scale[2]

			self.buildVertexFromCoords(posX, shape.scale, [False, True, True], index)
			self.buildVertexFromCoords(posY, shape.scale, [True, False, True], index)
			self.buildVertexFromCoords(posZ, shape.scale, [True, True, False], index)

		else:
			self.buildVertexFromCoords(shape.position, shape.scale, 
				[shape.scale[0] > 0, shape.scale[1] > 0, shape.scale[2] > 0], index)		


	def buildVertexFromCoords(self, pos, scale, axis, index):
		vertexBufferData = [
			[pos[0], pos[1], pos[2]],
			[pos[0] + scale[0]*(axis[0]&axis[1] or axis[0]&axis[2]), pos[1] + scale[1]*(axis[1]&axis[2]), pos[2]],
			[pos[0] + scale[0]*axis[0], pos[1] + scale[1]*axis[1], pos[2] + scale[2]*axis[2]],

			[pos[0], pos[1], pos[2]],
			[pos[0], pos[1] + scale[1]*(axis[0]&axis[1]), pos[2] + scale[2]*(axis[0]&axis[2] or axis[1]&axis[2])],
			[pos[0] + scale[0]*axis[0], pos[1] + scale[1]*axis[1], pos[2] + scale[2]*axis[2]]
		]

		textureBufferData = [
			[0.0, 0.0, index],
			[1.0 * (axis[0]&axis[1] or axis[0]&axis[2]), 1.0 * (axis[1]&axis[2]), index],
			[1.0, 1.0, index],

			[0.0, 0.0, index],
			[1.0*(axis[0]&axis[2] or axis[1]&axis[2]), 1.0*(axis[0]&axis[1]), index],
			[1.0, 1.0, index]
		]

		p1 = np.array(vertexBufferData[0], dtype = np.float32)
		p2 = np.array(vertexBufferData[1], dtype = np.float32)
		p3 = np.array(vertexBufferData[2], dtype = np.float32)
		face1 = common.Face(p1,p2,p3)

		p1 = np.array(vertexBufferData[3], dtype = np.float32)
		p2 = np.array(vertexBufferData[4], dtype = np.float32)
		p3 = np.array(vertexBufferData[5], dtype = np.float32)
		face2 = common.Face(p1,p2,p3)

		self.faces.append(face1)
		self.faces.append(face2)

		# print('kek:' + str(vertexBufferData))

		for vertex in vertexBufferData:
			self.vertexBuffer.append(vertex)

		for point in textureBufferData:
			self.textureBuffer.append(point)

	def buildNormalsFromFaces(self):
		for vertex in self.vertexBuffer:
			npVertex = np.array(vertex, dtype = np.float32)
			n = np.zeros(3, dtype = np.float32)
			i = 0
			for face in self.faces:
				if face.containsVertex(npVertex):
					n += face.normal
					i +=1
			n = common.normalize(n / i)
			self.normalBuffer.append(n)
