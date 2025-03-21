import graphics as g
import ppm
from graphics import Sphere, Plane, Point3D, Normal, ColorRGB

def determinePixelColor(obs, viewplane, camera, row, col, epsilon):
    # Create a ray that originates from the center point of a row/column on the viewing-plane (.orthographic_ray)
    ray = viewplane.perspective_ray(row, col, camera)

    # Intersect that ray with every object in the world by finding the hit point between the ray and object (.hit)
    counter = 0
    epsilon = 0.000001
    for obj in obs:
        hit = obj.hit(ray, epsilon)
        #print(f"col={col}, row={row} -> tmin={hit[1]}, ColorRGB{hit[3]}")
        # Keep track of:
        # Minimum t value
        # The particular object with the minimum t value, and that object's color
        if counter == 0 and hit[1] > epsilon:
            minT = hit[1]
            minObj = obj
            minColor = hit[3]
            counter += 1
        else:
            if epsilon < hit[1] < minT:
                minT = hit[1]
                minObj = obj
                minColor = hit[3]

    viewplane.set_color(row, col, minColor)

    print(f"col={col}, row={row} -> tmin={minT}, ColorRGB{minColor}")

    return minT, minObj, minColor

def raytraceChallenge(obs, viewplane, camera, epsilon, filename):
    myViewPlane = viewplane
    res = myViewPlane.get_resolution()
    hres = res[0]
    vres = res[1]

    #iterate through all rows and columns
    for i in range(vres):
        for j in range(hres):
            determinePixelColor(obs, myViewPlane, camera, i, j, epsilon)

    ppm.PPM(myViewPlane, filename)

# Build the Spheres that will be in our world
S1 = Sphere(Point3D(300,200,200), 100, ColorRGB(1.0,0.2,0.4))
S2 = Sphere(Point3D(-200,-100,50), 35, ColorRGB(0.3,0.8,0.2))
S3 = Sphere(Point3D(50,20,100), 25, ColorRGB(0.4,0.1,0.4))
S4 = Sphere(Point3D(300,-200,600), 250, ColorRGB(0.6,0.6,0.4))
S5 = Sphere(Point3D(400,400,900), 400, ColorRGB(0.0,0.2,1.0))

# Build the Planes that will be in our world
P1 = Plane(Point3D(50,50,999), Normal(0,0,1), ColorRGB(0.8,0.8,0.8))
P2 = Plane(Point3D(50,50,900), Normal(1,1,1), ColorRGB(1.0,1.0,1.0))

# It would make sense to put all of your objects into an array
# so that you can iterate through them.  Here is our observable world:
obs = [S1,S2,S3,S4,S5,P1,P2]

Camera1 = g.Ray(Point3D(0,0,-100), Normal(0,0,1))
raytraceChallenge(obs, g.ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0), Camera1, 0.000001, "part6img1.ppm")

Camera2 = g.Ray(Point3D(0,0,-1000), Normal(0,0,1))
raytraceChallenge(obs, g.ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0), Camera2, 0.000001, "part6img2.ppm")

Camera3 = g.Ray(Point3D(-100,-100,-30), Normal(0,0,1))
raytraceChallenge(obs, g.ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0), Camera3, 0.000001, "part6img3.ppm")