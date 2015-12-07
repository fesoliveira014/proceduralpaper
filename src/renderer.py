import numpy as np

from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, translate, rotate

import common
import camera

class Renderer(app.Canvas):
	def __init__(self, mesh, vertexShader, fragShader):
		app.Canvas.__init__(self, keys='interactive', size=(800,600))
		self.mesh = mesh
		self.data = mesh.buildBuffer()

		self.program = gloo.Program(vertexShader, fragShader)

		self.view = translate((-5, -5, -10))
		self.model = np.eye(4, dtype=np.float32)
		self.projection = perspective(45.0, self.size[0] /
                                      float(self.size[1]), 1.0, 1000.0)

		gloo.set_viewport(0, 0, self.size[0], self.size[1])

		self.camera = camera.Camera(np.array([0,0,-5], dtype = np.float32), np.array([0,0,0], dtype = np.float32), 45.0, self.size)

		self.program.bind(gloo.VertexBuffer(mesh.buildBuffer()))
		self.program['u_model'] = self.model
		self.program['u_view'] = self.view
		self.program['u_projection'] = self.projection

		gloo.set_depth_mask(True)
		gloo.set_state(blend=False, depth_test=True, polygon_offset_fill=True)

		self.show()

		self.theta = 0
		self.phi = 0

	def on_key_press(self, event):
		if event.text == 'k':
			self.model = np.dot(rotate(0.5, (0, 1, 0)), self.model)
			self.program['u_model'] = self.model

		if event.text == 'h' :
			self.theta -= .5
			self.model = np.dot(rotate(-0.5, (0, 1, 0)), self.model)
			self.program['u_model'] = self.model

		if event.text == 'u' :
			self.phi += .5
			self.model = np.dot(rotate(0.5, (1, 0, 0)), self.model)
			self.program['u_model'] = self.model

		if event.text == 'j' :
			self.phi -= .5
			self.model = np.dot(rotate(-0.5, (1, 0, 0)), self.model)
			self.program['u_model'] = self.model

		if event.text == 'r':
			self.phi = 0
			self.theta = 0
			self.model = np.eye(4, dtype=np.float32)
			self.program['u_model'] = self.model

		self.camera.onKeyPress(event)
		self.camera.update()
		self.view = self.camera.view
		self.program['u_view'] = self.view

		self.update()

	def on_key_release(self, event):
		self.camera.onKeyRelease(event)
		self.camera.update()
		self.view = self.camera.view
		self.program['u_view'] = self.view
		self.update()

	# def updateScene(self):
		
	# 	# self.update()

	def on_draw(self, event):
		gloo.clear('black')	
		# self.updateScene()
		self.program.draw('triangles')




	def run():
		app.run()