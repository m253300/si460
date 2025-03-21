# Caleb Koutrakos (m253300)
import numpy

# Vector3D Class
class Vector3D:
    # initializes a vector with 3 values such that it has x,y,z
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Vector3D")
    
    # converts vector to string
    def __str__(self):
        return str(self.v)
    
    # returns the sum of 2 vectors, overrides the '+' operator
    def __add__(self, other):
        if(isinstance(other, Vector3D)):
            return Vector3D(self.v + other.v)
        elif(isinstance(other, Normal)):
            return Normal(self.v[0] + other.n[0], self.v[1] + other.n[1], self.v[2] + other.n[2])
    
    # returns the difference of 2 vectors, overrides the '-' operator
    def __sub__(self, other):
        return Vector3D(self.v - other.v)
    
    # overrides the '*' operator
    # if argument is vector, returns dot product float
    # if argument is float, returns vector scaled up
    def __mul__(self, other):
        if(isinstance(other, float)):
            return Vector3D(self.v[0]*other, self.v[1]*other, self.v[2]*other)
        elif(isinstance(other, Vector3D)):
            return self.v[0]*other.v[0] + self.v[1]*other.v[1] + self.v[2]*other.v[2]
        
    # overrides '/' operator
    # returns vector divided by other vector
    def __truediv__(self, other):
        return Vector3D(self.v[0]/other, self.v[1]/other, self.v[2]/other)

    # returns copy of vector
    def copy(self):
        return Vector3D(self.v[0], self.v[1], self.v[2])
    
    # returns float magnitude of vector
    def magnitude(self):
        return numpy.sqrt(numpy.square(self.v[0]) + numpy.square(self.v[1]) + numpy.square(self.v[2]))

    # returns float square of a vector
    def square(self):
        return numpy.square(self.v[0]) + numpy.square(self.v[1]) + numpy.square(self.v[2])

    # returns float dot product of 2 vectors or vector and normal
    def dot(self, other):
        if(isinstance(other, Vector3D)):
            return self*other
        elif(isinstance(other, Normal)):
            return other*self

    # returns float dot product of 2 vectors at angle of each other
    def dotangle(self, other, angle):
        cosang = numpy.cos(angle*(numpy.pi/180))
        selfmag = self.magnitude()
        othmag = other.magnitude()
        return cosang * selfmag * othmag

    # returns vector cross product of 2 vectors
    def cross(self, other):
        u = self.v
        v = other.v
        first = u[1]*v[2]-u[2]*v[1]
        second = u[2]*v[0]-u[0]*v[2]
        third = u[0]*v[1]-u[1]*v[0]
        return Vector3D(first, second, third)
    
# Point3D Class
class Point3D:
    # initializes a point with 3 values such that it has x,y,z
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.p = val
        elif args and len(args) == 2:
            self.p = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Point3D")
        
    # converts point to string
    def __str__(self):
        return str(self.p)
    
    # returns the sum of point and vector 
    # overrides the '+' operator
    def __add__(self, other):
        return Point3D(self.p[0] + other.v[0], self.p[1] + other.v[1], self.p[2] + other.v[2])

    # overrides '-' operator
    # returns a point resulting from subtracting a vector
    # or returns a vector resulting from subtracting two points
    def __sub__(self, other):
        if(isinstance(other, Vector3D)):
            return Point3D(self.p[0] - other.v[0], self.p[1] - other.v[1], self.p[2] - other.v[2])
        elif(isinstance(other, Point3D)):
            return Vector3D(self.p[0] - other.p[0], self.p[1] - other.p[1], self.p[2] - other.p[2])

    # returns float distance squared between 2 points
    def distancesquared(self, other):
        return numpy.square(self.p[0]-other.p[0]) + numpy.square(self.p[1]-other.p[1]) + numpy.square(self.p[2]-other.p[2])

    # returns float distance between 2 points
    def distance(self, other):
        return numpy.sqrt(self.distancesquared(other))
    
    # returns copy of point
    def copy(self):
        return Point3D(self.p[0], self.p[1], self.p[2])
    
    # returns point scaled by a float
    # overrides '*'
    def __mul__(self, other):
        return Point3D(self.p[0]*other, self.p[1]*other, self.p[2]*other)
    
    # returns string representation of point3d
    def __repr__(self):
        return str(self.p)

# Normal Class
class Normal:
    # initializes a point with 3 values such that it has x,y,z
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.n = val
        elif args and len(args) == 2:
            self.n = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Normal")
        
    # converts normal to string
    def __str__(self):
        return str(self.n)
    
    # overrides negation operation '-'
    # outputs a normal
    def __neg__(self):
        return Normal(-self.n[0], -self.n[1], -self.n[2])
    
    # overrides addition operation '+'
    # outputs a normal from adding normals
    # or outputs a vector from adding a vector to a normal
    def __add__(self, other):
        if(isinstance(other, Normal)):
            return Normal(self.n[0] + other.n[0], self.n[1] + other.n[1], self.n[2] + other.n[2])
        elif(isinstance(other, Vector3D)):
            return Vector3D(self.n[0] + other.v[0], self.n[1] + other.v[1], self.n[2] + other.v[2])

    # overrides mult operation '*'
    # outputs a float from multiplying a normal by a vector
    # or outputs a normal by scaling a normal by a float
    def __mul__(self, other):
        if(isinstance(other, float)):
            return Normal(other * self.n[0], other * self.n[1], other * self.n[2])
        elif(isinstance(other, Vector3D)):
            return self.n[0] * other.v[0] + self.n[1] * other.v[1] + self.n[2] * other.v[2]

    # outputs a float by doing dot product between normal and vector
    def dot(self, other):
        return self * other
    
# Ray Class
class Ray:
    # initializes a ray with 2 values such that it has a Point3D and a Vector3D
    def __init__(self, origin, direction):
        if isinstance(origin, Point3D) and isinstance(direction, Vector3D):
            self.origin = origin
            self.direction = direction
        else:
            raise Exception("Invalid Arguments to Ray")
    
    # represents a ray in [[Origina], [Direction]] format
    def str(self):
        return '[' + str(self.origin) + ', ' + str(self.direction) + ']'
        
    # creates and returns a copy of the ray
    def copy(self):
        return Ray(self.origin, self.direction)
    
    # represents a ray in [[Origina], [Direction]] format
    def __repr__(self):
        return '[' + str(self.origin) + ', ' + str(self.direction) + ']'

# ColorRGB Class
class ColorRGB:
    # initializes a Color with 3 values such that it has r, g, b
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.c = numpy.round(val, 4)
        elif args and len(args) == 2:
            self.c = numpy.array([numpy.round(val, 4), numpy.round(args[0], 4), numpy.round(args[1], 4)], dtype='float64')
        else:
            raise Exception("Invalid Arguments to ColorRGB")
        
    # returns string representation of color
    def str(self):
        return str(self.c)
    
    # returns a copy of the color
    def copy(self):
        return ColorRGB(self.c[0], self.c[1], self.c[2])
    
    # returns string representation of color
    def __repr__(self):
        return str(self.c)
    
    # returns the RGB value of color
    def get(self, color):
        if color == 'R':
            return self.c[0]
        elif color == 'G':
            return self.c[1]
        elif color == 'B':
            return self.c[2]
        
    # adds two colors together
    # overrides '+'
    def __add__(self, other):
        return ColorRGB(self.c[0] + other.c[0], self.c[1] + other.c[1], self.c[2] + other.c[2])

    # multiply two colors values or multiply a colors values by a float or int
    # outputs a colorrgb
    #overrides '*'
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return ColorRGB(self.c[0] * other, self.c[1] * other, self.c[2] * other)
        elif isinstance(other, ColorRGB):
            return ColorRGB(self.c[0] * other.c[0], self.c[1] * other.c[1], self.c[2] * other.c[2])

    # divides a colors values by a float
    # overrides '/'
    def __truediv__(self, other):
        return ColorRGB(self.c[0] / other, self.c[1] / other, self.c[2] / other)

    # exponentiates a colors values by a float
    # overrides '**'
    def __pow__(self, other):
        return ColorRGB(self.c[0] ** other, self.c[1] ** other, self.c[2] ** other)

# Plane Class
class Plane:
    # initializes a plane with 3 values such that it has a Point3D, Vector3D and ColorRGB
    def __init__(self, point, normal, color=ColorRGB(1,1,1)):
        if isinstance(point, Point3D) and isinstance(normal, Normal) and isinstance(color, ColorRGB):
            self.point = point
            self.normal = normal
            self.color = color
        else:
            raise Exception("Invalid Arguments to Plane")
    
    # represents a plane in [[point], [normal]] format
    def str(self):
        return '[' + str(self.point) + ', ' + str(self.normal) + ']'
        
    # creates and returns a copy of the plane
    def copy(self):
        return Plane(self.point, self.normal, self.color)
    
    # represents a plane in [[point], [normal]] format
    def __repr__(self):
        return '[' + str(self.point) + ', ' + str(self.normal) + ']'
    
    # finds a hit point between a ray and this plane
    def hit(self, Ray, epsilon, shadeRec=False):
        retList = []

        a = self.point
        n = self.normal
        o = Ray.origin
        d = Ray.direction
        t = (n*(a-o))/(n*d)
        hitPt = o+d*t
        x = hitPt.p[0]
        y = hitPt.p[1]
        z = hitPt.p[2]
        if -epsilon <= x <= epsilon:
            x = 0
        if -epsilon <= y <= epsilon:
            y = 0
        if -epsilon <= z <= epsilon:
            z = 0
        hitPt = Point3D(x, y, z)
        planeColor = self.color

        if t < 0:
            isHit = False
        else:
            isHit = True

        retList.append(isHit)
        retList.append(t)
        retList.append(hitPt)
        retList.append(planeColor)

        return retList

# Tests all functionality of the Vector3D class
def testVector3D():
    print("\nTesting Vector3D:")

    c = 2.0
    v = Vector3D(1,2,3)
    u = Vector3D(4,5,6)

    print("Testing Printing...")
    if str(v) != '[1. 2. 3.]':
        raise Exception("Printing Error! " + str(v))

    print("Testing Addition...")
    if str(u+v) != '[5. 7. 9.]':
        raise Exception("Addition Error! " + str(u+v))
    
    print("Testing Subtraction...")
    if str(u-v) != '[3. 3. 3.]':
        raise Exception("Subtraction Error! " + str(u-v))
    
    print("Testing Scalar Multiplication...")
    if str(u*c) != '[ 8. 10. 12.]':
        raise Exception("Scalar Multiplication Error! " + str(u*c))
    
    print("Testing Scalar Division...")
    if str(u/c) != '[2.  2.5 3. ]':
        raise Exception("Scalar Multiplication Error! " + str(u/c))
    
    print("Testing Vector Copy...")
    if str(u.copy()) != '[4. 5. 6.]':
        raise Exception("Vector Copy Error! " + str(u.copy()))
    
    print("Testing Magnitude...")
    if str(numpy.round(u.magnitude(), 2)) != '8.77':
        raise Exception("Magnitude Error! " + str(u.magnitude()))
    
    print("Testing Square...")
    if str(u.square()) != '77.0':
        raise Exception("Square Error! " + str(u.square()))
    
    print("Testing Vector Multiplication...")
    if str(u*v) != '32.0':
        raise Exception("Vector Multiplication Error! " + str(u*v))
    
    print("Testing Vector Dot Product...")
    if str(u.dot(v)) != '32.0':
        raise Exception("Vector Dot Product Error! " + str(u.dot(v)))
    
    print("Testing Vector Dot Product w/ Angle...")
    if str(numpy.round(u.dotangle(v, 0), 2)) != '32.83':
        raise Exception("Vector Dot Product w/ Angle Error! " + str(u.dotangle(v, 0)))
    
    print("Testing Vector Dot Product w/ Angle...")
    if str(numpy.round(u.dotangle(v, 45), 2)) != '23.22':
        raise Exception("Vector Dot Product w/ Angle Error! " + str(u.dotangle(v, 45)))
    
    print("Testing Vector Dot Product w/ Angle...")
    if str(numpy.round(u.dotangle(v, 90), 0)) != '0.0':
        raise Exception("Vector Dot Product w/ Angle Error! " + str(numpy.round(u.dotangle(v, 90), 0)))

    print("Testing Cross Product...")
    if str(v.cross(u)) != '[-3.  6. -3.]':
        raise Exception("Cross Product Error! " + str(v.cross(u)))

# Tests all functionality of the Point3D class
def testPoint3D():
    print("\nTesting Point3D:")

    a = Point3D(1, 1, 1)
    b = Point3D(2, 2, 2)
    u = Vector3D(1, 2, 3)
    c = 2.0

    print("Testing Point+Vector Addition...")
    if str(a+u) != '[2. 3. 4.]':
        raise Exception("Point+Vector Addition Error! " + str(a+u))
    
    print("Testing Point-Vector Subtraction...")
    if str(a-u) != '[ 0. -1. -2.]':
        raise Exception("Point-Vector Subtraction Error! " + str(a-u))
    
    print("Testing Point-Point Subtraction...")
    if str(b-a) != '[1. 1. 1.]':
        raise Exception("Point-Point Subtraction Error! " + str(b-a))
    
    print("Testing Point Distance Squared...")
    if str(a.distancesquared(b)) != '3.0':
        raise Exception("Point Distance Squared Error! " + str(a.distancesquared(b)))
    
    print("Testing Point Distance...")
    if str(numpy.round(a.distance(b), 2)) != '1.73':
        raise Exception("Point Distance Error! " + str(numpy.round(a.distance(b), 2)))
    
    print("Testing Point Copy...")
    if str(a.copy()) != '[1. 1. 1.]':
        raise Exception("Point Copy Error! " + str(a.copy()))
    
    print("Testing Point Multiplication...")
    if str(a*c) != '[2. 2. 2.]':
        raise Exception("Cross Product Error! " + str(a*c))

# Tests all functionality of the Normal class
def testNormal():
    print("\nTesting Normal:")

    c = 2.0
    u = Vector3D(1, 1, 1)
    n = Normal(2, 2, 2)
    m = Normal(3, 3, 3)

    print("Testing Normal Negation...")
    output = str(-n)
    if output != '[-2. -2. -2.]':
        raise Exception("Normal Negation Error! " + output)
    
    print("Testing Normal+Normal...")
    output = str(n+m)
    if output != '[5. 5. 5.]':
        raise Exception("Normal+Normal Error! " + output)
    
    print("Testing Normal*Vector...")
    output = str(n*u)
    if output != '6.0':
        raise Exception("Normal*Vector Error! " + output)
    
    print("Testing Normal.dot(Vector)...")
    output = str(n.dot(u))
    if output != '6.0':
        raise Exception("Normal.dot(Vector) Error! " + output)
    
    print("Testing Vector.dot(Normal)...")
    output = str(u.dot(n))
    if output != '6.0':
        raise Exception("Vector.dot(Normal) Error! " + output)
    
    print("Testing Float*Normal...")
    output = str(n*c)
    if output != '[4. 4. 4.]':
        raise Exception("Float*Normal Error! " + output)
    
    print("Testing Normal+Vector...")
    output = str(n+u)
    if output != '[3. 3. 3.]':
        raise Exception("Normal+Vector Error! " + output)
    
    print("Testing Vector+Normal...")
    output = str(u+n)
    if output != '[3. 3. 3.]':
        raise Exception("Vector+Normal Error! " + output)

# Tests all functionality of the Ray class
def testRay():
    print("\nTesting Ray:")

    point = Point3D(2, 2, -2)
    vector = Vector3D(0, 0, 1)
    ray = Ray(point, vector)

    print("Testing Ray Copy...")
    output = ray.copy()
    if str(output) != str(ray):
        raise Exception("Ray Copy Error! " + str(output))
    
    print("Testing Ray String Representation...")
    output = ray.__repr__()
    if str(output) != '[[ 2.  2. -2.], [0. 0. 1.]]':
        raise Exception("Ray String Representation Error! " + output)

# Tests all functionality of the ColorRGB class
def testColorRGB():
    print("\nTesting ColorRGB:")

    c1 = ColorRGB(0, 0, 1)
    c2 = ColorRGB(1, 0, 0)
    c3 = ColorRGB(0.3, 0.5, 0.8)
    n = 2.0

    print("Testing copy()...")
    output = c1.copy()
    if str(output) != str(c1):
        raise Exception("copy() Error! " + str(output))
    
    print("Testing __repr__()...")
    output = c1.__repr__()
    if output != "[0. 0. 1.]":
        raise Exception("__repr__ Error! " + output)
    
    print("Testing get()...")
    output = c1.get('R')
    if str(output) != "0.0":
        raise Exception("get() Error! " + str(output))
    
    print("Testing __add__(color)...")
    output = c1 + c2
    if str(output) != "[1. 0. 1.]":
        raise Exception("__add(color)__ Error! " + str(output))
    
    print("Testing __mul__(color)...")
    output = c1 * c2
    if str(output) != "[0. 0. 0.]":
        raise Exception("__mul__(color) Error! " + str(output))
    
    print("Testing __mul__(float)...")
    output = c1 * n
    if str(output) != "[0. 0. 2.]":
        raise Exception("__mul__(float) Error! " + str(output))

    print("Testing __truediv__(float)...")
    output = c1 / n
    if str(output) != "[0.  0.  0.5]":
        raise Exception("__truediv__(float) Error! " + str(output))
    
    print("Testing __pow__(float)...")
    output = c3 ** n
    if str(output) != "[0.09 0.25 0.64]":
        raise Exception("__pow__(float) Error! " + str(output))

# Tests all functionality of the Plane class
def testPlane():
    print("\nTesting Plane:")

    point = Point3D(0, 0, 0)
    normal = Normal(1, 1, 1)
    plane = Plane(point, normal)

    print("Testing copy()...")
    output = plane.copy()
    if str(output) != str(plane):
        raise Exception("copy() Error! " + str(output))
    
    print("Testing __repr__()...")
    output = plane.__repr__()
    if output != "[[0. 0. 0.], [1. 1. 1.]]":
        raise Exception("__repr__() Error! " + output)
    
    planeHit = Plane(Point3D(2, 4, 2), Normal(-3, -3, -2))
    ray = Ray(Point3D(1, 1, -10), Vector3D(2, 2, 4))

    print("Testing hit()...")
    output = planeHit.hit(ray, 0.0001)
    if output[0] != True and output[1] != 1.8 and str(output[2]) != '[ 4.6  4.6 -2.8]' and str(output[3]) != '[1. 1. 1.]':
        raise Exception("hit() Error! " + str(output))

#tests all class methods
if __name__ == '__main__':
    testVector3D()
    testPoint3D()
    testNormal()
    testRay()
    testColorRGB()
    testPlane()