#version 330 core

// Input vertex data, different for all executions of this shader.
attribute vec3 a_position;
attribute vec4 a_color;
attribute vec3 a_texture;

// Output data ; will be interpolated for each fragment.
out vec3 UV;

// Values that stay constant for the whole mesh.
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

void main(){

	// Output position of the vertex, in clip space : MVP * position
	gl_Position =  u_projection * u_view * u_model * vec4(a_position,1);
	
	// UV of the vertex. No special space for this one.
	UV = a_texture;
}