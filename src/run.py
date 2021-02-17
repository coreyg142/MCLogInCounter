"""MCLoginCounter

This script reads Minecraft server log files from a /data directory and counts the number of times each
player has logged in.

It prints out the results in a formatted table as well as printing to the console

"""

import os

# the amount of padding to add in the output
_OUTPUT_PADDING = 5
# the folder the data is in
_DATA_DIRECTORY = 'data'
# the folder to print the output to
_OUTPUT_DIRECTORY = 'output'
# the file to print the output to
_OUTPUT_FILE = 'output.txt'
# the message to print when /output/ does not exist
_OUTPUT_DIR_MADE = "Output folder not found, creating one..."
# the message to print when /data/ does not exist
_DATA_DIR_ERR = "Data directory not found. I have created a data folder, please populate it with log files and try " \
                "again "
# the message to print when /data/ is empty
_DATA_DIR_EMPTY = "Your data directory is empty. Please populate it with log files and try again"


def getName(line):
    """Returns the username to count
    :prerequisite : assumes the input line is in the format:

    "[TIMESTAMP] [Server thread/INFO]: USERNAME[/IP_ADDRESS] logged in with entity id ENTITY_ID at ([world]X_COORD,
    Y_COORD, Z_CORD)"

    :param line : str
        The console log line to read the name from
    :returns name : str
        The username of the player who logged in
    """
    # Get the "USERNAME[/IP_ADDRESS]" portion of the string
    temp = line.split(" ")[3]
    # Get the "USERNAME" portion of the string
    name = temp.split("[")[0]
    return name


def countName(name, nameDict):
    """Counts a given username

    :param nameDict : nameDict
        The dictionary of Username/Count key/value pairs
    :param name : str
        The name to count
    """
    if name not in nameDict:
        # add an entry initialized at 1 appearance
        nameDict[name] = 1
    else:
        # increment an existing entry
        nameDict[name] += 1


def writeTableFile(nameDict, directory, file):
    """Given a key/value pair dictionary, writes the data to a file in a formatted table in the format:

    "Name_________________No. of logins"

    :param directory : str
        The directory to write to
    :param file : str
        The file to write to
    :param nameDict : nameDict
        The key/value dictionary containing the data to write
    """
    # Calculate the column width based on the longest name element
    colWidth = max(len(str(element)) for pair in nameDict for element in pair) + _OUTPUT_PADDING

    # The first line of the table
    outT = ("Name", "No. of logins")
    outS = outT[0].ljust(colWidth, '_') + outT[1].rjust(len(outT[1])) + '\n'

    # Loop through the dict and add that data to the output
    for pair in nameDict:
        outS = outS + justify(pair, colWidth) + '\n'

    # Open the directory and write to the file

    ensureDirWrite(directory, _OUTPUT_DIR_MADE)
    outF = open(directory + '/' + file, "w")
    outF.write(outS)
    outF.close()


def printTableConsole(nameDict):
    """Given a key/value pair dictionary, writes the data to the console in a formatted table of the format:

    "Name_________________No. of logins"

    :param nameDict : dict
        The dictionary containing the data to output"""
    outT = ("Name", "No. of logins")

    colWidth = max(len(str(element)) for pair in nameDict for element in pair) + _OUTPUT_PADDING

    print(outT[0].ljust(colWidth, '_') + outT[1].rjust(len(outT[1])))
    for pair in nameDict:
        print(justify(pair, colWidth))


def justify(pair, colWidth):
    """A helper method that assists in formatting the output in a consistent manner.
    Takes a colWidth and adds enough padding characters to reach that width

    :param pair : tuple
        The (name, count) tuple containing data to format
    :param colWidth : int
        The width that the output str should be
    :returns str
        The formatted string"""
    return pair[0].ljust(colWidth, '_') + str(pair[1])


def ensureDirWrite(filePath, printout):
    """Helper method to ensure the file path we are writing to exists. Make the directory if it does not

    :param filePath : str
        The path to check
    :param printout : str
        The message to print if the path does not exist"""
    if not os.path.exists(filePath):
        print(printout)
        os.mkdir(filePath)


def ensureDirRead(filePath, printout):
    """Helper method to ensure the file path we are reading from exists. If it does not, make the directory
    and stop the script

    :param filePath : str
        The path to check
    :param printout : str
        The message to print if the path does not exist"""
    if not os.path.exists(filePath):
        print(printout)
        os.mkdir(filePath)
        exit()


def main():
    # The dictionary to store Name/Count pairs
    nameDict = {}
    directory = _DATA_DIRECTORY
    totalCount = 0
    # Ensure the data directory exists, create and exit if not
    ensureDirRead(directory, _DATA_DIR_ERR)
    # List the files in the data directory
    dirList = os.listdir(directory)
    # If there are none, print and exit
    if len(dirList) == 0:
        print(_DATA_DIR_EMPTY)
        exit()
    # Loop through all the files
    for filename in dirList:
        fullDir = directory + '/' + filename
        # If it is a log file, open it and iterate through the lines
        if filename.endswith(".log"):
            f = open(fullDir, 'r', encoding="utf8")
            for line in f:
                # if the line is a log in event, identify user and increment their count
                if "logged in with entity id" in line:
                    name = getName(line)
                    countName(name, nameDict)
                    totalCount += 1
            f.close()

    # Sort the dictionary by count highest to lowest
    sorted_dict = sorted(nameDict.items(), key=lambda x: x[1], reverse=True)

    # Print the final count
    if len(sorted_dict):
        printTableConsole(sorted_dict)
        writeTableFile(sorted_dict, _OUTPUT_DIRECTORY, _OUTPUT_FILE)


if __name__ == '__main__':
    main()
