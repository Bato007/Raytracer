from vectors import *
from figures import *

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.normal = []
        self.faces = []
        self.triangles = []
        self.read()

    def read(self):
        for line in  self.lines:
            try:
                if line:
                    prefix, value = line.split(' ', 1)

                    # Se separan
                    if prefix == 'v':
                        self.vertices.append(
                            list(map(float, value.split(' ')))
                        )
                    elif prefix == 'vn':
                        self.normal.append(
                            list(map(float, value.split(' ')))
                        )
                    elif prefix == 'f':
                        self.faces.append(
                            [list(map(int, face.split('/'))) for face in value.split(' ')]
                        )
            except:
                pass
    
    def loadTriangles(self, material, move=(0, 0, 0), scale=(1, 1, 1)):
        for face in self.faces:
            f = face[0][0] - 1
            dot = self.vertices[f]
            for i in range(len(dot)): dot[i] = (dot[i] * scale[i]) + move[i]
            A = V3(*dot)
            f = face[1][0] - 1
            dot = self.vertices[f]
            for i in range(len(dot)): dot[i] = (dot[i] * scale[i]) + move[i]
            B = V3(*dot)
            f = face[2][0] - 1
            dot = self.vertices[f]
            for i in range(len(dot)): dot[i] = (dot[i] * scale[i]) + move[i]
            C = V3(*dot)
            f = face[3][0] - 1
            dot = self.vertices[f]
            for i in range(len(dot)): dot[i] = (dot[i] * scale[i]) + move[i]
            D = V3(*dot)

            # Ahora las normales
            tn = face[0][2] - 1
            normal = self.normal[tn]      
            nA = V3(*normal)
            tn = face[1][2] - 1
            normal = self.normal[tn]      
            nB = V3(*normal)
            tn = face[2][2] - 1
            normal = self.normal[tn]      
            nC = V3(*normal)
            tn = face[0][2] - 1
            normal = self.normal[tn]      
            nD = V3(*normal)

            self.triangles.append(Triangle(points=(A, B, C), normals=(nA, nB, nC), material=material))
            self.triangles.append(Triangle(points=(A, C, D), normals=(nA, nC, nD), material=material))
        return self.triangles
