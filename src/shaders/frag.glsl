
#version 330 core

// Interpolated values from the vertex shaders
in vec3 UV;
in vec3 Normal;
in vec3 FragPos;

// Ouput data
out vec4 color;

// Uniforms
uniform vec3 u_lightPos; 
uniform vec3 u_lightColor;

// Values that stay constant for the whole mesh.

void main(){

    float ambientStrength = 1f;
    vec3 ambient = ambientStrength * u_lightColor;

    // vec3 norm = normalize(Normal);
    // vec3 lightDir = normalize(u_lightPos - FragPos);
    // float diff = max(dot(norm, lightDir), 0.0);
    // vec3 diffuse = diff * u_lightColor;

	// Output color = color of the texture at the specified UV

    vec3 texColor;

	if (UV.z == float(0))
		texColor = vec3(0.5f, 0.5f, 0.5f);
	else if (UV.z == float(1))
		texColor = vec3(0.4f, 0.4f, 0.4f);
	else if (UV.z == float(2))
		texColor = vec3(0.3f, 0.3f, 0.3f);
	else if (UV.z == float(3))
		texColor = vec3(0.2f, 0.2f, 0.2f);

    vec3 result = (ambient) * texColor;
    color = vec4(result, 1.0f);

}