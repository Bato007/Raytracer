from lib import *
from figures import *
from vectors import *
from obj import *
from math import pi, tan

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, width, height, background_color=BLACK):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.light = None
        self.clear()

    def clear(self):
        self.pixels = [
            [BLACK for _ in range(self.width)]
            for _ in range(self.height)
        ]
    
    def write(self, filename):
        writeBMP(filename, self.width, self.height, self.pixels)

    def point(self, x, y, paint_color):
        self.pixels[y][x] = paint_color

    def cast_ray(self, origin, direction, recursion=0):
        material, intersect = self.scene_intersect(origin, direction)

        if not material or recursion >= MAX_RECURSION_DEPTH: 
            return self.background_color

        light_dir = (self.light.position - intersect.point).normal()
        light_distance = (self.light.position - intersect.point).len()

        # Shadows
        offset_normal = (intersect.normal * 1.1)

        # Para espejos
        if material.albedo[2] > 0:
            reverse_direction = direction * -1
            reflect_direction = reflect(reverse_direction, intersect.normal)
            reflect_origin = (intersect.point - offset_normal) if (reflect_direction ** intersect.normal) < 0 else (intersect.point + offset_normal)
            reflect_color = self.cast_ray(reflect_origin, reflect_direction, recursion + 1)
        else:
            reflect_color = color(0, 0, 0)

        if material.albedo[3] > 0:
            refraction_direction = refract(direction, intersect.normal, material.refractive_index)
            refract_origin = (intersect.point - offset_normal) if (refraction_direction ** intersect.normal) < 0 else (intersect.point + offset_normal)
            refract_color = self.cast_ray(refract_origin, refraction_direction, recursion + 1)
        else:
            refract_color = color(0, 0, 0)

        shadow_origin = (intersect.point - offset_normal) if (light_dir ** intersect.normal) < 0 else (intersect.point + offset_normal)
        shadow_material, shwadow_intersect = self.scene_intersect(shadow_origin, light_dir)
        shadow_intensity = 0

        if shadow_material and (((shwadow_intersect.point - shadow_origin).len()) < light_distance):
            shadow_intensity = 0.9

        intensity = self.light.intensity * max(0, (light_dir ** intersect.normal)) * (1 - shadow_intensity)

        specular_reflection = reflect(light_dir, intersect.normal)
        speular_intensit = self.light.intensity * (
            max(0, (specular_reflection ** direction))**material.spec
        )

        # Para crear el color
        diffuse_color = material.getColor()
        albedo = material.getAlbedo()
        diffuse = diffuse_color * intensity * albedo[0]
        specular = color(255, 255, 255) * speular_intensit * albedo[1]
        reflection = reflect_color * albedo[2]
        refraction = refract_color * albedo[3]

        return diffuse + specular + reflection + refraction

    def scene_intersect(self, origin, direction):
        zbuffer = float('inf')
        material = None
        intersect = None

        for obj in self.scene:
            r_intersect = obj.ray_intersect(origin, direction)     
            if r_intersect and r_intersect.distance < zbuffer: 
                zbuffer = r_intersect.distance
                material = obj.material
                intersect = r_intersect
        return material, intersect

    def render(self):
        fov = int(pi/2)
        tfov = tan(fov/2)
        for y in range(self.height):
            for x in range(self.width):
                i = ((2*x + 1 - self.width) / self.height) * tfov
                j = (1 - ((2*y + 1) / self.height)) * tfov

                # Para pintar
                direction = V3(i, j, -1).normal()
                paint_color = self.cast_ray(V3(0, 0, 0), direction)
                self.point(x, y, paint_color)

r = Raytracer(200, 200, color(135, 206, 235))
r.light = Light(
    position=V3(-5, -20, 10), 
    intensity=2
)

ivory = Material(color(100, 100, 80), albedo=[0.6, 0.3, 0.1, 0], spec=50)
rubber = Material(color(80, 0, 0), albedo=[0.9, 0.1, 0, 0], spec=10)
mirror = Material(color(255, 255, 255), albedo=[0, 10, 0.8, 0], spec=1500)
glass = Material(color(150, 180, 200), albedo=(0, 0.5, 0.1, 0.8), spec=125, refractive_index=1.5)
iron = Material(color(129,126,121), albedo=[0.95, 0.01, 0.3, 0], spec=100)

model = Obj('./block.obj')
triangles = model.loadTriangles(rubber, (-1, -2, -5))

r.scene = [
    Cube(V3(3, 3, -15), V3(2, 3, 7), ivory),
    Cube(V3(3, 1, -8), V3(2, 2, 2), glass),
    Cube(V3(2, 2, -20), V3(8, 5, 1), mirror),
    Cube(V3(3, -4, -17), V3(5, 5, 5), iron),
    Triangle((V3(0, 4, -7), V3(2, 3, -5), V3(-4, -3, -30)), (V3(0, 0, 1), V3(0, 0, 1), V3(0, 0, 1)), rubber)
]
# r.scene = triangles
# r.scene = []

r.render()
r.write('out')