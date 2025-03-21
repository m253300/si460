Caleb Koutrakos
253300

Part 1:
The order of operations does matter because Case 1 and 2 produce different scenes and likewise for Case 3 and 4
Case 1 - Rotated it 45 degrees around the z axis, moved it to the right in the y-axis, and then moved it "back" in the z-axis
Case 2 - moved it to the right in the y-axis, rotated it 45 degrees around the z-axis, and then moved it back in the z-axis
Case 3 - Scaled it by 3 in the y, rotated it 45 degrees around the z axis, and moved it back in the z by 15
Case 4 - Rotated it around the z axis 45 degrees, scaled it by 3 in the y, and moved it back in the z
These modify the matrix via calculations and order of operations matter

Part 2:
[
    x
    y
    z + 20.0
    1
]

The actual order of transforms is reverse. So it rotated, scaled and translated rather than the way it was written

Part 3:
glTranslatef(20.0, 8.0, -15.0)
glRotatef(45.0, 0.0, 0.0, 1.0)

Part 4:
glTranslatef(-7.0, 0.0, -15.0)
WireCube(5.0)

glTranslatef(14.0, 0.0, 0.0)
WireCube(5.0)

glTranslatef(-7.0, -7.0, 0.0)
WireCube(5.0)

glTranslatef(0.0, 14.0, 0.0)
WireCube(5.0)