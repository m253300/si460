# Caleb Koutrakos (m253300)
import numpy

class Vector3D:
# Vector3D Class
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
        if(isinstance(other, float) or isinstance(other, int)):
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
        if isinstance(other, Vector3D):
            v = other.v
        elif isinstance(other, Normal):
            v = other.n
        first = u[1]*v[2]-u[2]*v[1]
        second = u[2]*v[0]-u[0]*v[2]
        third = u[0]*v[1]-u[1]*v[0]
            
        return Vector3D(first, second, third)
    
class Point3D:
# Point3D Class
    # initializes a point with 3 values such that it has x,y,z
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Point3D")
        
    # converts point to string
    def __str__(self):
        return str(self.v)
    
    # returns the sum of point and vector 
    # overrides the '+' operator
    def __add__(self, other):
        return Point3D(self.v[0] + other.v[0], self.v[1] + other.v[1], self.v[2] + other.v[2])

    # overrides '-' operator
    # returns a point resulting from subtracting a vector
    # or returns a vector resulting from subtracting two points
    def __sub__(self, other):
        if(isinstance(other, Vector3D)):
            return Point3D(self.v[0] - other.v[0], self.v[1] - other.v[1], self.v[2] - other.v[2])
        elif(isinstance(other, Point3D)):
            return Vector3D(self.v[0] - other.v[0], self.v[1] - other.v[1], self.v[2] - other.v[2])

    # returns float distance squared between 2 points
    def distancesquared(self, other):
        return numpy.square(self.v[0]-other.v[0]) + numpy.square(self.v[1]-other.v[1]) + numpy.square(self.v[2]-other.v[2])

    # returns float distance between 2 points
    def distance(self, other):
        return numpy.sqrt(self.distancesquared(other))
    
    # returns copy of point
    def copy(self):
        return Point3D(self.v[0], self.v[1], self.v[2])
    
    # returns point scaled by a float
    # overrides '*'
    def __mul__(self, other):
        return Point3D(self.v[0]*other, self.v[1]*other, self.v[2]*other)
    
    # returns string representation of point3d
    def __repr__(self):
        return str(self.v)

class Normal:
# Normal Class
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
    
class Ray:
# Ray Class
    # initializes a ray with 2 values such that it has a Point3D and a Vector3D
    def __init__(self, origin, direction):
        if isinstance(origin, Point3D) and (isinstance(direction, Vector3D) or isinstance(direction, Normal)):
            self.origin = origin
            if isinstance(direction, Vector3D):
                self.direction = direction
            else:
                self.direction = Vector3D(direction.n[0], direction.n[1], direction.n[2])
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

class ColorRGB:
# ColorRGB Class
    # initializes a Color with 3 values such that it has r, g, b
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = numpy.round(val, 4)
        elif args and len(args) == 2:
            self.v = numpy.array([numpy.round(val, 4), numpy.round(args[0], 4), numpy.round(args[1], 4)], dtype='float64')
        else:
            raise Exception("Invalid Arguments to ColorRGB")
        
    # returns string representation of color
    def str(self):
        return str(self.v)
    
    # returns a copy of the color
    def copy(self):
        return ColorRGB(self.v[0], self.v[1], self.v[2])
    
    # returns string representation of color
    def __repr__(self):
        return str(self.v)
    
    # returns the RGB value of color
    def get(self):
        return self.v[0], self.v[1], self.v[2]
        
    # adds two colors together
    # overrides '+'
    def __add__(self, other):
        return ColorRGB(self.v[0] + other.v[0], self.v[1] + other.v[1], self.v[2] + other.v[2])

    # multiply two colors values or multiply a colors values by a float or int
    # outputs a colorrgb
    #overrides '*'
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return ColorRGB(self.v[0] * other, self.v[1] * other, self.v[2] * other)
        elif isinstance(other, ColorRGB):
            return ColorRGB(self.v[0] * other.v[0], self.v[1] * other.v[1], self.v[2] * other.v[2])

    # divides a colors values by a float
    # overrides '/'
    def __truediv__(self, other):
        return ColorRGB(self.v[0] / other, self.v[1] / other, self.v[2] / other)

    # exponentiates a colors values by a float
    # overrides '**'
    def __pow__(self, other):
        return ColorRGB(self.v[0] ** other, self.v[1] ** other, self.v[2] ** other)

class Plane:
# Plane Class
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
        x = hitPt.v[0]
        y = hitPt.v[1]
        z = hitPt.v[2]
        if -epsilon <= x <= epsilon:
            x = 0
        if -epsilon <= y <= epsilon:
            y = 0
        if -epsilon <= z <= epsilon:
            z = 0
        hitPt = Point3D(x, y, z)
        planeColor = self.color

        if t < epsilon:
            isHit = False
        else:
            isHit = True

        retList.append(isHit)
        retList.append(t)
        retList.append(hitPt)
        retList.append(planeColor)

        return retList

class Sphere:
# Sphere Class
    # initializes a sphere with 3 values such that it has a Point3D, radius float and ColorRGB
    def __init__(self, centerPoint, radius, color=ColorRGB(1,1,1)):
        if isinstance(centerPoint, Point3D) and (isinstance(radius, float) or isinstance(radius, int)) and isinstance(color, ColorRGB):
            self.center = centerPoint
            self.radius = float(radius)
            self.color = color
        else:
            raise Exception("Invalid Arguments to Sphere")
    
    # represents a sphere in [[centerPoint], radius] format
    def str(self):
        return '[' + str(self.center) + ', ' + str(self.radius) + ']'
        
    # creates and returns a copy of the sphere
    def copy(self):
        return Sphere(self.center, self.radius, self.color)
    
    # represents a sphere in [[centerPoint], radius] format
    def __repr__(self):
        return '[' + str(self.center) + ', ' + str(self.radius) + ']'
    
    # finds a hit point between a ray and this sphere
    def hit(self, ray, epsilon, shadeRec=False):
        # prepare empty list for returning 4 values of different types
        retList = []

        # prepare values which will be easily be used in math
        d = ray.direction
        o = ray.origin
        c = self.center
        r = self.radius

        aq = d*d
        bq = (o-c)*d*2
        cq = (o-c).square() - r**2

        # calculate if there is a hit using discriminant
        disc = bq**2 - 4*aq*cq
        # disc < 0 means no hit, so return t=0
        if disc < 0:
            t = 0
        # disc = 0 means 1 hit, so return tpos if t>epsilon
        elif disc == 0:
            t = (-bq + disc**0.5)/(2*aq)
        # disc > 0 means 2 hits, so return smaller t>epsilon
        else:
            tpos = (-bq + disc**0.5)/(2*aq)
            tneg = (-bq - disc**0.5)/(2*aq)
            # two positive t's; return smaller t
            if tpos > 0 and tneg > 0:
                if tpos < tneg:
                    t = tpos
                else:
                    t = tneg
            # two negative t's: return bigger t
            elif tpos < 0 and tneg < 0:
                if tpos > tneg:
                    t = tpos
                else:
                    t = tneg
            # one negative t, one positive t; return positive t
            else:
                if tpos < 0:
                    t = tneg
                else:
                    t = tpos

        if t > epsilon:
            isHit = True
        else:
            isHit = False

        # calculate point where ray hits sphere
        hitPt = o + d*t

        # determine the x,y,z values of the point where the hit 
        x = hitPt.v[0]
        y = hitPt.v[1]
        z = hitPt.v[2]

        # ensure the calculated values are not basically zero
        if -epsilon <= x <= epsilon:
            x = 0
        if -epsilon <= y <= epsilon:
            y = 0
        if -epsilon <= z <= epsilon:
            z = 0

        # create a point to return
        hitPt = Point3D(x, y, z)

        # get the color of the sphere at the hit location
        sphereColor = self.color

        # add all values to list to be returned
        retList.append(isHit)
        retList.append(t)
        retList.append(hitPt)
        retList.append(sphereColor)

        # return list of values determined from if the ray hits the sphere
        return retList

class ViewPlane:
# ViewPlane Class
    # initializes a ViewPlane with center point, normal vector, horizontal resolution, vertical resolution, and pixel size/scale
    def __init__(self, center, normal, hres, vres, pixelsize):
        if isinstance(center, Point3D) and isinstance(normal, Normal) and isinstance(hres, int) and isinstance(vres, int) and (isinstance(pixelsize, float) or isinstance(pixelsize, int)):
            self.center = center
            self.normal = normal
            self.grid = [[ColorRGB(0., 0., 0.) for i in range(hres)] for k in range(vres)]
            self.hres = hres #col
            self.vres = vres #row
            self.pixelsize = float(pixelsize)

            c = self.center
            n = self.normal
            width = self.hres
            height = self.vres
            scale = self.pixelsize

            Vup = Vector3D(0., -1., 0.)

            self.u = (Vup.cross(-n))/((Vup.cross(-n)).magnitude())

            self.v = self.u.cross(-n)

            self.LL = c - self.u*(width/2.0)*scale - self.v*(height/2.0)*scale
        else:
            raise Exception("Invalid Arguments to ViewPlane")
        
    # .get_color(row, col) - Retrieve the ColorRGB object located at position (x, y).
    def get_color(self, row, col):
        return self.grid[row][col]
    
    # .set_color(row, col, ColorRGB-Object) - Set a specific pixel's value to the ColorRGB object.
    def set_color(self, row, col, color):
        self.grid[row][col] = color
    
    # .get_point(row, col) - Return a Point3D object that is located at the center of the specific pixel.
    def get_point(self, row, col):
        LL = self.LL
        scale = self.pixelsize
        u = self.u
        v = self.v
        row = float(row)
        col = float(col)
        point = LL + u*(col+0.5)*scale + v*(row+0.5)*scale

        return point
    
    # .get_resolution() - Retrieve the horizontal and vertical values for the size of the viewing plane, this should return both numbers back individually.
    def get_resolution(self):
        return self.hres, self.vres

    # .orthographic_ray(row, col) - Find the point at the center of a specific pixel in the viewing plane. This can be considered the ray's origin for the purposes of drawing our scene, use this point and the ViewPlane's normal to build and return a Ray Object.
    def orthographic_ray(self, row, col):
        #return a ray using the point calculated through get_point and the viewplane's normal vector
        origin = self.get_point(row, col)
        n = self.normal
        direction = Vector3D(n.n[0], n.n[1], n.n[2])
        return Ray(origin, direction)
    
    # .perspective_ray(row, col, Ray-Object-Camera-Origin) - Find the position of the center of a pixel, use this and the position of the Camera (the Ray object) to determine the appropriate direction for the new perspective based ray that will be used to draw the scene.
    def perspective_ray(self, row, col, rayObjCamOrigin):
        origin = self.get_point(row, col)
        #direction = rayObjCamOrigin.direction
        # or its the difference between the calculated origin point and the ray's origin
        direction = origin - rayObjCamOrigin.origin
        return Ray(origin, direction)

def testVector3D():
# Tests all functionality of the Vector3D class
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
    if str(numpy.round(u.square(), 1)) != '77.0':
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

def testPoint3D():
# Tests all functionality of the Point3D class
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
    if str(numpy.round(a.distancesquared(b), 1)) != '3.0':
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

def testNormal():
# Tests all functionality of the Normal class
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

def testRay():
# Tests all functionality of the Ray class
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

def testColorRGB():
# Tests all functionality of the ColorRGB class
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
    output = c1.get()
    if str(output) != "(0.0, 0.0, 1.0)":
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

def testPlane():
# Tests all functionality of the Plane class
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
    if (output[0] != True) or (output[1] != 1.8) or (str(output[2]) != '[ 4.6  4.6 -2.8]') or (str(output[3]) != '[1. 1. 1.]'):
        raise Exception("hit() Error! " + str(output))

def testSphere():
# Tests all functionality of the Sphere class
    print("\nTesting Sphere:")

    point = Point3D(0, 2, 4)
    radius = 10.0
    color = ColorRGB(1, 1, 1)
    sphere = Sphere(point, radius, color)

    print("Testing copy()...")
    output = sphere.copy()
    if str(output) != str(sphere):
        raise Exception("copy() Error! " + str(output))
    
    print("Testing __repr__()...")
    output = sphere.__repr__()
    if output != "[[0. 2. 4.], 10.0]":
        raise Exception("__repr__() Error! " + output)
    
    ray = Ray(Point3D(1, 1, -10), Vector3D(2, 2, 4))

    print("Testing hit()...")
    output = sphere.hit(ray, 0.000001)
    if (output[0] != True) or (output[1] != 1.1666666666666667) or (str(output[2]) != '[ 3.33333333  3.33333333 -5.33333333]') or (str(output[3]) != '[1. 1. 1.]'):
        raise Exception("hit() Error! " + str(output))

def testViewPlane():
# Tests all functionality of the ViewPlane class
    print("\nTesting ViewPlane:")

    vp = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0)
    print(str(['debug 1',0,0,vp.get_point(0,0)]))
    print(str(['debug 2',479,639,vp.get_point(479,639)]))

    vp = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0)
    print(str(vp.get_point(0, 0)))
    print(str(vp.get_point(250, 100)))

    vp = ViewPlane(Point3D(0,0,0), Normal(1,1,-1), 640, 480, 1.0)
    print(str(vp.get_point(0, 0)))
    print(str(vp.get_point(250, 100)))

    vp = ViewPlane(Point3D(0,0,0), Normal(1,1,-1), 640, 480, 1)
    print(str(vp.get_point(0, 0)))
    print(str(vp.get_point(250, 100)))

    print(str(vp.orthographic_ray(0, 0)))

#tests class methods
if __name__ == '__main__':
    testVector3D()
    testPoint3D()
    testNormal()
    testRay()
    testColorRGB()
    testPlane()
    testSphere()
    testViewPlane()