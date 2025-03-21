from graphics import Sphere, Plane, Point3D, Normal, ColorRGB, ViewPlane

def determinePixelColor(obs, viewplane, row, col, epsilon):
    # Create a ray that originates from the center point of a row/column on the viewing-plane (.orthographic_ray)
    ray = viewplane.orthographic_ray(row, col)

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


if __name__ == '__main__':
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

    col = 639
    row = 479
    viewplane = ViewPlane(Point3D(0, 0, 0), Normal(0, 0, 1), 640, 480, 1.0)

    determinePixelColor(obs, viewplane, row, col, 0.000001)