
#version 330 core

// Interpolated values from the vertex shaders
in vec3 UV;

// Ouput data
out vec4 color;

// Values that stay constant for the whole mesh.

void main(){

	// Output color = color of the texture at the specified UV
	if (UV.z == float(0))
		color = vec4(0.5, 0.5, 0.5, 1);
	else if (UV.z == float(1))
		color = vec4(0.4, 0.4, 0.4, 1);
	else if (UV.z == float(2))
		color = vec4(0.3, 0.3, 0.3, 1);
	else if (UV.z == float(3))
		color = vec4(0.2, 0.2, 0.2, 1);
}