# plane with point 2,4,2 and normal -3,-3,-2
# ray with point 1,1,-10 and vector 2,2,4
# t = (a-o)n/(d*n)
# a = plane point
# n = plane normal
# o = ray point
# d = ray vector

import graphics

a = plPt = graphics.Point3D(2, 4, 2)
n = plNorm = graphics.Normal(-3, -3, -2)

o = rayPt = graphics.Point3D(1, 1, -10)
d = rayVect = graphics.Vector3D(2, 2, 4)

print(a-o)
# = (1, 3, 12)

print(n*(a-o))
# = -36

print(n*d)
# = -20

print("t = " + str((n*(a-o))/(n*d)))
t = (n*(a-o))/(n*d)
# t = 1.8

print(d*t)
# = (3.6, 3.6, 7.2)

print("hit point = " + str(o+d*t))
p = o+d*t
# = (4.6, 4.6, -2.8)

# In order to calculate the final point, and the t-value,
# my classes can only interpret specific orders of vectors, floats, etc.
# Such as d*t, where d is a vector and t is a float, I can only interpret
# vector*float and not float*vector so when calculating p=o+td it gives an error
# but p=o+dt works.