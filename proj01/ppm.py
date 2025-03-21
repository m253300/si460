def PPM(viewplane, filename):
    f = open(filename, "w")

    f.write("P3\n")

    res = viewplane.get_resolution()
    hres = res[0]
    vres = res[1]
    f.write(str(hres) + " " + str(vres) + "\n")

    f.write("255")

    #loop through grid
    for i in range(vres-1, -1, -1):
        #newline
        f.write("\n")
        for j in range(hres):
            #convert 0-1 scale to 0-255 scale and print
            color = viewplane.get_color(i, j).get()
            red = int(color[0]*255)
            green = int(color[1]*255)
            blue = int(color[2]*255)
            f.write(f"{red} {green} {blue}\t")

    f.close()