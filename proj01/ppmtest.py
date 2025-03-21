import graphics as g
from ppm import PPM

myViewPlane = g.ViewPlane(g.Point3D(0,0,0), g.Normal(0,0,1), 3, 4, 1)
myViewPlane.set_color(0,0,g.ColorRGB(1,1,1))
myViewPlane.set_color(0,2,g.ColorRGB(1,0,0))
myViewPlane.set_color(1,1,g.ColorRGB(1,0,1))
myViewPlane.set_color(1,2,g.ColorRGB(1,1,0))
myViewPlane.set_color(3,0,g.ColorRGB(0,1,0))
myViewPlane.set_color(3,2,g.ColorRGB(0,0,1))

PPM(myViewPlane, 'part3-testing.ppm')