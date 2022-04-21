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