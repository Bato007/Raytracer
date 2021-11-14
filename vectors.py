class V3(object):
    def __init__(self, x=0, y=0, z=0):
        # print(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'V3(%s, %s, %s)' %(self.x, self.y, self.z)

    # Para sumar vectores
    def __add__(self, o):
        try:
            return V3(
                self.x + o.x,
                self.y + o.y,
                self.z + o.z
            )
        except:
            return V3(
                self.x + o,
                self.y + o,
                self.z + o
            ) 

    def __sub__(self, o):
        return V3(
            self.x - o.x,
            self.y - o.y,
            self.z - o.z
        )

    def __mul__(self, c):
        x = self.x * c
        y = self.y * c
        z = self.z * c
        return V3(x, y, z)

    # CrossProduct
    def __truediv__(self, c):
        x = self.x / c
        y = self.y / c
        z = self.z / c
        return V3(x, y, z)

    # PointProduct
    def __pow__(self, o):
        return ((self.x * o.x) + (self.y * o.y) + (self.z * o.z))

    def len(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def normal(self):
        length = self.len()

        if length == 0:
            return V3(0, 0, 0)

        return V3(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def reciprocal(self):
        return V3(
            9999999 if self.x == 0 else 1 / self.x,
            9999999 if self.y == 0 else 1 / self.y,
            9999999 if self.z == 0 else 1 / self.z
        )

def reflect(I, N):
    return (I - (N*((I**N)*2))).normal()

def refract(I, N, refractive_index):
    cosi = -max(-1, min(1, I ** N))
    etai = 1
    etat = refractive_index

    if cosi < 0:    # Adentro del objeto
        cosi = -cosi
        etai, etat = etat, etai
        N = N * -1

    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if (k < 0):
        return V3(1, 0, 0)
    
    return ((I*eta) + (N * (eta * cosi - k**(1/2)))).normal()

def barycentric(A, B, C, P):
    result = V3(C.x - A.x, B.x - A.x, A.x - P.x) // V3(C.y - A.y, B.y - A.y, A.y - P.y)
    cx, cy, cz = result.cx, result.cy, result.cz

    if cz == 0: return -1, -1, -1

    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return w, v, u
