import graphics as g
import raytracer_part4 as raytracer
import ppm
from graphics import Sphere, Plane, Point3D, Normal, ColorRGB

def raytrace(obs, viewplane, epsilon, filename):
    myViewPlane = viewplane
    res = myViewPlane.get_resolution()
    hres = res[0]
    vres = res[1]

    #iterate through all rows and columns
    for i in range(vres):
        for j in range(hres):
            raytracer.determinePixelColor(obs, myViewPlane, i, j, epsilon)

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

raytrace(obs, g.ViewPlane(Point3D(0,0,0), Normal(0,0,1), 200, 100, 1.0), 0.000001, "part5img1.ppm")
raytrace(obs, g.ViewPlane(Point3D(50,50,-50), Normal(0,0,1), 200, 100, 1.0), 0.000001, "part5img2.ppm")
raytrace(obs, g.ViewPlane(Point3D(50,50,-50), Normal(1,1,1), 200, 100, 1.0), 0.000001, "part5img3.ppm")
raytrace(obs, g.ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0), 0.000001, "part5img4.ppm")
raytrace(obs, g.ViewPlane(Point3D(50,50,-50), Normal(-0.2,0,1), 200, 100, 1.0), 0.000001, "part5img5.ppm")