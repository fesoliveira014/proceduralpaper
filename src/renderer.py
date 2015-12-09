import numpy as np

from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, translate, rotate

import common
import camera

class Renderer(app.Canvas):
	def __init__(self, mesh, vertexShader, fragShader):
		app.Canvas.__init__(self, keys='interactive', size=(1600,900))
		self.mesh = mesh
		self.data = mesh.buildBuffer()

		self.program = gloo.Program(vertexShader, fragShader)

		self.model = np.eye(4, dtype=np.float32)
		self.projection = perspective(45.0, self.size[0] /
                                      float(self.size[1]), 1.0, 1000.0)

		gloo.set_viewport(0, 0, self.size[0], self.size[1])

		self.camera = camera.Camera(np.array([0,0,-5], dtype = np.float32), np.array([0,0,0], dtype = np.float32), 45.0, self.size)

		self.view = self.camera.view

		self.program.bind(gloo.VertexBuffer(mesh.buildBuffer()))
		self.program['u_model'] = self.model
		self.program['u_view'] = self.view
		self.program['u_projection'] = self.projection

		self.program['u_lightPos'] = np.array([20, 20, -20], dtype = np.float32);
		self.program['u_lightColor'] = np.array([1, 1, 1], dtype = np.float32);

		gloo.set_depth_mask(True)
		gloo.set_blend_func('src_alpha', 'one_minus_src_alpha') 
		gloo.set_blend_equation('func_add')
		gloo.set_cull_face('back')
		gloo.set_front_face('cw')

		gloo.set_state(blend=True, depth_test=True, polygon_offset_fill=True)

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

	def on_key_release(self, event):
		self.camera.onKeyRelease(event)
		self.camera.update()

	def on_mouse_press(self, event):
		self.camera.onMousePress(event)
		self.camera.update()

	def on_mouse_release(self,event):
		self.camera.onMouseRelease(event)
		self.camera.update()

	# def on_mouse_move(self, event):
	# 	self.camera.onMouseMove(event)
	# 	self.camera.update()

	def on_draw(self, event):
		self.view = self.camera.view
		self.program['u_view'] = self.view
		self.update()
		gloo.clear([0.7, 0.7, 0.7])	
		self.program.draw('triangles')




	def run():
		app.run()