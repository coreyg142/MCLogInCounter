import os


def getName(line):
    temp = line.split(" ")[3]
    name = temp.split("[")[0]
    return name


def countName(name, dict):
    if name not in dict:
        dict[name] = 1
    else:
        dict[name] += 1


def writeTableFile(dict, dir):
    col_width = max(len(str(element)) for pair in dict for element in pair) + 5

    outT = ("Name", "No. of logins")
    outS = outT[0].ljust(col_width, '_') + outT[1].rjust(len(outT[1])) + '\n'

    for pair in dict:
        outS = outS + justify(pair, col_width) + '\n'

    outF = open(dir, "w")
    outF.write(outS)
    outF.close()



def printTableConsole(dict):
    outT = ("Name", "No. of logins")

    col_width = max(len(str(element)) for pair in dict for element in pair) + 5

    print(outT[0].ljust(col_width, '_') + outT[1].rjust(len(outT[1])))
    for pair in dict:
        print(justify(pair, col_width))


def justify(pair, col_width):
    return pair[0].ljust(col_width, '_') + str(pair[1])


def main():
    os.chdir('../')
    nameDict = {}
    directory = 'data'
    totalCount = 0
    for filename in os.listdir(directory):
        fullDir = directory + '\\' + filename
        if filename.endswith(".log"):
            f = open(fullDir, 'r', encoding="utf8")
            for line in f:
                if "logged in with entity id" in line:
                    name = getName(line)
                    countName(name, nameDict)
                    totalCount += 1
            f.close()

    sorted_dict = sorted(nameDict.items(), key=lambda x: x[1], reverse=True)

    if len(sorted_dict):
        printTableConsole(sorted_dict)
        writeTableFile(sorted_dict, "output\\output.txt")


if __name__ == '__main__':
    main()
