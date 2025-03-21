class census:

    #Takes in a file and extracts the required data
    def __init__(self, givenFile):
        self.inputFile = givenFile
        rawData = []
        with open(givenFile, "r") as file:
            for line in file:
                line = line[213:316]
                rawData.append(line)

        sortedData = []

        for x in rawData:
            num = x[:13].strip()
            loc = x[13:]
            sortedData.append(loc + "|||||" + num)

        sortedData.sort()

        self.locData = []
        self.numData = []
        self.fileData = []

        for x in sortedData:
            locnum = x.split("|||||")
            self.locData.append(locnum[0].strip())
            self.numData.append(locnum[1])
            self.fileData.append(locnum[1].ljust(21) + locnum[0].strip())
    
    #Displays all the required data line by line
    def display(self):
        for x in self.fileData:
            print(x)

    #Searches for and prints a data entry specified by a data number
    def searchByNum(self, num):
        index = self.numData.index(str(num))
        print(self.fileData[index])

    #Searches for and prints a data entry specified by a location
    def searchByDistrict(self, loc):
        index = self.locData.index(str(loc))
        print(self.fileData[index])