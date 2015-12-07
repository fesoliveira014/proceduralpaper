import common
import ruleParser
import modelBuilder
import meshBuilder
import renderer

from vispy import app

grammar = ruleParser.Parser("../ruleset2.txt")

builder = modelBuilder.ModelBuilder()
builder.buildModel(grammar.ruleset)

meshbuilder = meshBuilder.MeshBuilder()
meshbuilder.buildMeshFromTree(builder.tree)

mesh = common.Mesh(meshbuilder.vertexBuffer, meshbuilder.textureBuffer)

vertexShader = ""
with open("shaders/vertex.glsl", "r") as f:
	vertexShader = f.read()

fragShader = ""
with open("shaders/frag.glsl", "r") as f:
	fragShader = f.read()

canvas = renderer.Renderer(mesh, vertexShader, fragShader)

app.run()


