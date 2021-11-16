from vectors import *
from lib import *

EPSILON = 0.0001

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def ray_intersect(self, origin, direction):
        L = self.center - origin
        tca = L ** direction      # Product point
        l = L.len()

        d2 = l**2 - tca**2
        if d2 > self.radius**2:   # Verifica si esta afuera
            return None

        thc = (self.radius**2 - d2)**(1/2)

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0: t0 = t1
        if t0 < 0: return None

        hit = (direction*t0) + origin
        normal = (hit - self.center).normal()

        return Intersect(
            distance=t0,
            normal=normal,
            point=hit
        )

class Quadrilateral(object):
    def __init__(self, minbound, maxbound, material):
        self.min = minbound
        self.max = maxbound
        self.material = material
    
    def ray_intersect(self, origin, direction):
        idirection = direction.reciprocal()
        if (idirection.x >= 0):
          tmin = (self.min.x - origin.x) * idirection.x
          tmax = (self.max.x - origin.x) * idirection.x
        else:
          tmin = (self.max.x - origin.x) * idirection.x
          tmax = (self.min.x - origin.x) * idirection.x
        
        if (idirection.y >= 0):
          tymin = (self.min.y  - origin.y) * idirection.y
          tymax = (self.max.y - origin.y) * idirection.y
        else:
          tymin = (self.max.y - origin.y) * idirection.y
          tymax = (self.min.y - origin.y) * idirection.y


        if (tmin > tymax) or (tymin > tmax): return None
        if (tymin > tmin): tmin = tymin
        if (tymax < tmax): tmax = tymax

        # if (idirection.z >= 0):
        #   tzmin = (self.min.z - origin.z) * idirection.z
        #   tzmax = (self.max.z - origin.z) * idirection.z
        # else:
        #   tzmin = (self.max.z - origin.z) * idirection.z
        #   tzmax = (self.min.z - origin.z) * idirection.z

        # if (tmin > tzmax) or (tzmin > tmax): return None
        # if (tzmin > tmin): tmin = tzmin
        # if (tzmax < tmax): tmax = tzmax

        hit = (direction * tmin) + origin

        return Intersect (
            distance=tmin,
            normal=V3(0.7, 0.7, 0.7),
            point=hit
        )

class Plane(object):
    def __init__(self, y, material):
        self.y = y
        self.material = material

    def ray_intersect(self, orig, direction):
        d = (orig.y + self.y) / direction.y
        pt = orig + (direction * d)

        if d <= 0 or abs(pt.x) > 2 or pt.z > -5 or pt.z < -10:
            return None

        normal = V3(0, 1, 0)

        return Intersect(
            distance=d,
            point=pt,
            normal=normal
        )

class Face(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal
        self.material = material
    
    def ray_intersect(self, origin, direction):
        den = direction ** self.normal
        if abs(den) > 0.01:
            d = (self.normal ** (self.position - origin)) / den
            if d > 0:
                hit = origin + (direction * d)
                return Intersect(
                    distance = d,
                    point= hit,
                    normal= self.normal
                )

class Cube(object):
    def __init__(self, center, size, material):
        self.center = center
        self.material = material
        self.min = center - ((size/2) + EPSILON)
        self.max = center + ((size/2) + EPSILON)
        self.faces = []

        # Faces
        self.faces.append(Face(center + V3(size.x/2, 0, 0), V3(1, 0, 0), material))
        self.faces.append(Face(center + V3(-size.x/2, 0, 0), V3(-1, 0, 0), material))

        self.faces.append(Face(center + V3(0, size.y/2, 0), V3(0, 1, 0), material))
        self.faces.append(Face(center + V3(0, -size.y/2, 0), V3(0, -1, 0), material))

        self.faces.append(Face(center + V3(0, 0, size.z/2), V3(0, 0, 1), material))
        self.faces.append(Face(center + V3(0, 0, -size.z/2), V3(0, 0, -1), material))

    def ray_intersect(self, orig, dir):
        intersect = None
        d = float('inf')

        for face in self.faces:
            hited = face.ray_intersect(orig, dir)
            if hited:
                # Si estoy dentro de los bounds
                
                if hited.point.x < self.min.x or self.max.x < hited.point.x: continue
                if hited.point.y < self.min.y or self.max.y < hited.point.y: continue
                if hited.point.z < self.min.z or self.max.z < hited.point.z: continue
                
                #Si soy el plano mas cercano
                if hited.distance < d:
                    d = hited.distance
                    intersect = Intersect(
                        distance = d,
                        point = hited.point,
                        normal = hited.normal
                    )
        return intersect

class Triangle(object):
    def __init__(self, points, material):
        self.A, self.B, self.C = points
        self.center = (points[0] + points[1] + points[2]) / 3
        self.normal = V3(*crossProduct((self.B - self.A), (self.C - self.A))).normal()
        self.material = material
    
    def __repr__(self):
        return '%s, %s, %s' %(self.A, self.B, self.C)

    def ray_intersect(self, origin, direction):
        den = direction ** self.normal
        if abs(den) > 0.01:
            d = (self.normal ** (self.center - origin)) / den
            if d > 0:
                hit = origin + (direction * d)

                # Here goes de varicentric
                w, v, u = barycentric(self.A, self.B, self.C, hit)
                if w < 0 or v < 0 or u < 0: return None

                return Intersect(
                    distance = d,
                    point= hit,
                    normal= self.normal
                )
