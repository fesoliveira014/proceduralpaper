import common
import meshBuilder

class MeshBuilder():
	def __init__(self):
		self.vertexBuffer = []
		self.textureBuffer = []
		self.queue = []
		self.shapeList = []
		self.isTraversalOver = False

	def buildMeshFromTree(self, tree):
		self.queue.append(tree)
		self.buildShapeList()
		self.buildVertexBuffer()


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

		# print('kek:' + str(vertexBufferData))

		for vertex in vertexBufferData:
			self.vertexBuffer.append(vertex)

		for point in textureBufferData:
			self.textureBuffer.append(point)