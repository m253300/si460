rawData = []
with open("mdgeo2010.dp", "r") as file:
    for line in file:
        line = line[213:316]
        rawData.append(line)

sortedData = []

for x in rawData:
    num = x[:13].strip()
    loc = x[13:]
    sortedData.append(loc + "|||||" + num)

sortedData.sort()

for x in sortedData:
    locnum = x.split("|||||")
    print(locnum[1].ljust(21) + locnum[0])