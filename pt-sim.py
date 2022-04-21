# Team Name: SegFault
# Partners: Phi Do, Erika Mendoza, Brandon Luna
# Class: CS450
# Date: 4/21/2022
# Description: Project that simulates a page table, address translation, and is 
# then expanded into simulating algorithms such as the clock / second chance algorithm

#---------------- Modules being import ----------------#

# sys: This module provides access to some variables used or maintained by 
# the interpreter and to functions that interact strongly with the interpreter. 

# getopt: C-style parser for command line options

# Math: This module provides access to the mathematical functions defined
# by the C standard.
import getopt, sys, math

#------------------------------------------------------#

#-------------------- Background on Input file ---------------------#
# pages[0] gives three values:  N M SIZE                            #
# N(virtN) is the number of bits in the virtual address             #
# M(physM) is the number of bits in the physical address            #
# SIZE(pageSize) is the size of a page in bytes                     #
#                                                                   #
# page[row][i] are each a single row of the page table:  V P F U    #
# V is an ASCII char (1/0) representing if the page is valid or not #
# (1 indicates the page is in memory)                               #
# P is an ASCII char (0–7) representing the access permissions      #
# (0 means no access, anything else is permitted                    #
# F is the frame number                                             #
# U is an ASCII char (1/0) representing if the page has been        #
# recently used (this can be ignored for Part A)                    #
#-------------------------------------------------------------------#

#--------------------------------------------------------------#
#               Class to handle table elements                 #
#--------------------------------------------------------------#
class PageTable:
    def __init__(self,infile):
        self.virtN = 0
        self.physM = 0
        self.pageSize = 0
        self.pages = [] # Used as a 2-D array 
        self.ptr = 0

        # Handling File Opening
        file = open(infile, 'r')

        # Splits input accordingly as long as there is no endline
        # appends tokens into array of pages
        for token in file:
            if token != '\n':
                c = token.split()
                self.pages.append(c)

        first = False
        second = False

        # Virtual and Physical Address Size Logic
        for i in self.pages[0]:
            if not first:
                self.virtN = int(i)
                first = True

            elif first and not second:
                self.physM = int(i)
                second = True

            else:
                self.pageSize = int(i)

        self.pages.pop(0)   # Discarding initial 

        # Allocating Pointer to correct pages
        for i in range(int(math.log(self.pageSize, 2)) - 1):
            if self.pages[i][0]:
                self.ptr = i
                break

#------------- End of Class Initialization -------------#

    #-------------- Start of Getter Functions --------------#
    def printData(self):
        print("Virtual Address Size: ", self.virtN)
        print("Physical Address Size: ", self.physM)
        print("Page Size: ", self.pageSize)

    def printPages(self):
        print(self.virtN, " ", self.physM, " ", self.pageSize)
        for i in self.pages:
            print(i)

    def fetchPages(self):
        return self.pages

    def fetchVirtualSize(self):
        return self.virtN

    def fetchPhysicalSize(self):
        return self.physM

    def fetchPageSize(self):
        return self.pageSize

    def fetchValidPage(self, row):
        return self.pages[row][0]

    def fetchAccessBit(self, row):
        decToBin = dec2bin(int(self.pages[row][1])) # Converts curr decimal to 10 bit binary
        return decToBin

    def fetchFrameNumber(self, row):
        return self.pages[row][2]

    def fetchRecentlyUsed(self, row):
        return self.pages[row][3]

    #------------- End of Getter Functions -------------#

#--------------------------------------------------------------#
#               Usage Function for help info                   #
#--------------------------------------------------------------#
def usage():
    print("Usage:\n\n")
    print("--help: Provides usage information for both commands and arguments")
    print("--verbose: Provides information about what is being outputted")
    print("--test: Allows for tests to type conversion (e.g decimal to hex)")
    print("-c: sets clock flag to True")

#--------------------------------------------------------------#
#               Argument Checking Function                     #
#--------------------------------------------------------------#
def validArgs(argv):
    try:
        # Parses command line options and parameter list
        options, arguments = getopt.getopt(argv, 'c', ['help', 'test', 'verbose'])
    
    # Thrown when unrecognized option is entered
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    flags = [False, False, False]   # Flag Array to handle parameters

    for opt, arg in options:
        if opt in ['--help']:
            usage()

        elif opt in ['--verbose']:
            flags[0] = True

        elif opt in ['--test']:
            flags[1] = True

        elif opt in ['c']:
            flags[2] = True

    return flags

#--------------------------------------------------------------#
#               Test Flag Function                             #
# (Called when test flag is set to true to do num conversion)  #
#--------------------------------------------------------------#

def test():

    def info():
        print("Enter 'exit' to terminate testing mode / program")
        print("Additional info for testing mode \n type 'info'")
        return

    info()

    h = False
    dec = False

    while True:
        userInput = input()

        if userInput.lower() == "exit":
            print("Exiting testing mode and program...")

        if userInput.lower() == "info":
            info()

        if h:
            print("Binary: ", hex2bin(userInput))
            print("Decimal: ", hex2dec(userInput))
            print("Binary back to Hexidecimal: ", bin2hex(userInput))

        elif dec:
            print("Binary: ", dec2bin(userInput))
            print("Decimal: ", dec2hex(userInput))
            print("Binary back to Decimal: ", bin2hex(userInput))

#--------- Start of Number Check and Coversion Functions (Hex/Dec/Bin) ---------#

def checkNum(num):

    if num[:2] == "0x":
        h = "hex"
        return h

    else:
        d = "dec"
        return d

def hex2dec(n):
    return int(n, 16)
    
def dec2hex(n):
    n = int(n, base=10)
    return hex(n)
    
def hex2bin(n):
    n = int(n, base=16)
    return bin(n)

def bin2hex(n):
    n = int(n, base=2)
    return hex(n)

def bin2dec(n):
    n = int(n, base=2)
    return int(n)

def dec2bin(n):
    n = bin(int(n))
    return n[2:]

#--------- End of Number Check and Coversion Functions (Hex/Dec/Bin) ---------#

#--------------------------------------------------------------#
#                   Valid Page Function                        #
#        (Validates if address is in page table)               #
#--------------------------------------------------------------#

def valPage(virtN, physM):
    if type(virtN) == int:
        virtN = str(virtN)
    if '0' in virtN:
        if physM != 0:
            return "DISK"
        else:
            return "SEGFAULT"
    else:
        return False

#--------------------------------------------------------------#
#              Virt to Phys Address Function                   #
#        (Translates Virtual Address to Physical Address       #
#        Using the Clock Algorithm                     )       #
#--------------------------------------------------------------#

def clockVirt2Phys(pageTable, virtualAddr):
    numberType = checkNum(virtualAddr)
    pageSize = pageTable.fetchPageSize()
    virtualSize = pageTable.fetchVirtualSize()
    indxSize = int(virtualSize - math.log(pageTable.pageSize, 2))
    numPages = math.log(pageTable.pageSize, 2)
    pageFault = "PAGEFAULT"

    # Hex to Binary Conversion
    if numberType == "hex":
        virtualBinary = hex2bin(virtualAddr)[2:]
        if len(virtualBinary) < virtualSize:   
            while len(virtualBinary) < virtualSize: # Adds 0's in front of string
                virtualBinary = "0" + virtualBinary
        append = virtualBinary[indxSize:]   # Virt Offset
        pageTableIndex = virtualBinary[:indxSize]   # Page

    # Decimal to Binary Conversion
    else:
        virtualBinary = hex2bin(dec2hex(virtualAddr))[2:]
        if len(virtualBinary) < virtualSize:
            while len(virtualBinary) < virtualSize:
                virtualBinary = "0" + virtualBinary
        append = virtualBinary[indxSize:]   # Virt Offset
        pageTableIndex = virtualBinary[:indxSize]   # Page  

    # Valid Index checking
    if pageTable.pages[pageTable.ptr][0] == 1:
        return virt2phys(pageTable, virtualAddr)

    # Checking and Updating Table
    for i in range(pageTable.ptr+1, int(numPages)-1):

        if int(pageTable.pages[i][3]) == 0:
            pageTable.pages[i][0] = 0 # update valid inex
            pageTable.pages[pageTable.ptr][0] = 1 # update valid pointer
            pageTable.pages[pageTable.ptr][2] = pageTable.pages[i][2] # update frame ptr
            pageTable.pages[pageTable.ptr][3] = 1

            pageTable.ptr += 1

            if(pageTable.ptr > numPages):
                for i in range(pageTable.ptr - 1):
                    if pageTable.pages[i][0]:
                        pageTable.ptr = i
            return "PAGEFAULT"

        else:
            pageTable.ptr += 1
            
            if(pageTable.ptr > numPages):
                for i in range(pageTable.ptr - 1):
                    if pageTable.pages[i][0]:
                        pageTable.ptr = i
            return virt2phys(pageTable, virtualAddr)

#--------------------------------------------------------------#
#                 Virt to Phys Address Function                #
#--------------------------------------------------------------#

def virt2phys(pageTable, virtualAddr):
    numberType = checkNum(virtualAddr)
    # print("Type: ",numberType)
    pageSize = pageTable.fetchPageSize()
    virtualSize = pageTable.fetchVirtualSize()
    indxSize = int(virtualSize - math.log(pageTable.pageSize, 2))

    # Hex to Binary Conversion
    if numberType == "hex":
        virtualBinary = hex2bin(virtualAddr)[2:]
        if len(virtualBinary) < virtualSize:   
            while len(virtualBinary) < virtualSize: # Adds 0's in front of string
                virtualBinary = "0" + virtualBinary
        append = virtualBinary[indxSize:]   # Virt Offset
        pageTableIndex = virtualBinary[:indxSize]   # Page

    # Decimal to Binary Conversion
    else:
        virtualBinary = hex2bin(dec2hex(virtualAddr))[2:]
        if len(virtualBinary) < virtualSize:
            while len(virtualBinary) < virtualSize:
                virtualBinary = "0" + virtualBinary
        append = virtualBinary[indxSize:]   # Virt Offset
        pageTableIndex = virtualBinary[:indxSize]   # Page  

    indx = bin2dec(pageTableIndex)  # Page in Decimal
    physMBit = bin2dec(pageTable.fetchAccessBit(indx))    # Permission Bit
    frameToBin = hex2bin(dec2hex(pageTable.fetchFrameNumber(indx))) # Frame to Binary
    virtNBit = pageTable.fetchValidPage(indx)

    valid = valPage(virtNBit, physMBit)

    if valid:
        return valid
    
    virt2phy = frameToBin + append # Frame + Offset

    # Translating Virt Address to Phys Address in type of Int
    if numberType == "hex":
        phys = bin2hex(virt2phy)
    else:
        phys = bin2dec(virt2phy)
    return phys

def readIn(flags, pageTable):

    print("Type 'quit' to terminate program")

    if(flags[2]):
        for line in sys.stdin:
            if line.lower() == 'quit':
                return
            clockAlg = clockVirt2Phys(pageTable, line)
            print(clockAlg)
    else:
        for line in sys.stdin:
            if line.lower() == 'quit':
                return
            phys = virt2phys(pageTable, line)
            print(phys)
    return

#--------------------------------------------------------------#
#                 Main Function                                #
#--------------------------------------------------------------#

def main(argv):
    # flags[0] = verbose, flgas[1] = test, flags[2] = c

    flags = validArgs(argv)

    infile = argv[-1]

    if flags[0]: 
        print('inFile: ', infile)
        print("Reading in file....")

    pageTable = PageTable(infile)
    # pageTable.printPages()
    # pageTable.printData()

    readIn(flags, pageTable)
    print("Terminating Program....")

    return

if __name__ == "__main__":
    main(sys.argv[1:])