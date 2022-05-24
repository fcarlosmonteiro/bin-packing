import sys
import binpacking
import matplotlib.pyplot as plt

# Number of desidered equal balanced bins

def create_resources():
   #return a dict
   resources = {
      "A" : 5, "B" : 5, "C" : 3, "D" : 4, 
      "E" : 4, "F" : 1, "G" : 4, "H" : 5, 
      "I" : 4, "L" : 3, "M" : 3, "N" : 4,
      "O" : 3, "P" : 2, "Q" : 3, "R" : 1,
      "S" : 5, "T" : 2, "U" : 5, "V" : 3,
      "Z" : 1,
   }
   return resources

