
import struct

class Material(object):
    def __init__(self, diffuse, albedo, spec, refractive_index=0):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec
        self.refractive_index = refractive_index
    
    def getColor(self):
        return self.diffuse
    
    def getAlbedo(self):
        return self.albedo

class Intersect(object):
    def __init__(self, distance, normal, point):
        self.distance = distance
        self.normal = normal
        self.point = point

class Light(object):
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other_color):
        r = self.r + other_color.r
        g = self.g + other_color.g
        b = self.b + other_color.b

        return color(r, g, b)

    def __mul__(self, other):
        r = self.r * other
        g = self.g * other
        b = self.b * other
        return color(r, g, b)

    def __repr__(self):
        return "color(%s, %s, %s)" % (self.r, self.g, self.b)

    def toBytes(self):
        self.r = int(max(min(self.r, 255), 0))
        self.g = int(max(min(self.g, 255), 0))
        self.b = int(max(min(self.b, 255), 0))
        return bytes([self.b, self.g, self.r])

    __rmul__ = __mul__

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

def char(c):
    # ocupa 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short, ocupa 2 bytes
    return struct.pack('=h', w)

def dword(dw):
    # long, ocupa 4 bytes
    return struct.pack('=l', dw)

def writeBMP(filename, width, height, pixels):
    filename += '.bmp'
    f = open(filename, 'bw')
    # file header ' siempre es BM y ocupa 14 bytes
    f.write(char('B'))
    f.write(char('M'))
    # Se multiplica por tres por ser rgb
    f.write(dword(54 + 3*(width*height)))
    f.write(dword(0))
    f.write(dword(54))  # En donde

    # info header '
    f.write(dword(40))  # Tamaño del info header
    f.write(dword(width)) 
    f.write(dword(height))
    f.write(word(1))    # pela pero se pone
    f.write(word(24))   # Siempre es 24
    f.write(dword(0))   # pela
    f.write(dword(3*(width*height)))

    for _ in range(4):        # Cosas que pelan
        f.write(dword(0))

    # bitmap
    for y in range(height):
        for x in range(width):
            f.write(pixels[y][x].toBytes())

    f.close()
