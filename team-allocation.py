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

def run_greedy(resources,numberOfBins):
   groups = binpacking.to_constant_bin_number(resources, numberOfBins)
   print(groups)
   
   #print only the groups
   resourcesPerGroups = [list(group.keys()) for group in groups]
   print(resourcesPerGroups)
   return groups

def analysis(resources,groups,numberOfBins):
   # the optimal average desired value 
   idealValue = sum(resources.values()) / numberOfBins    # 

   # value of the groups obtained
   realValues = [sum(group.values()) for group in groups]

   return idealValue,realValues

def visualization(idealValue, realValues,numberOfBins):
   fig, ax = plt.subplots(1, 1, figsize = (16,6))

   # Plots
   ax.bar(x = range(numberOfBins), height = realValues, color="#408090")
   ax.hlines(idealValue, -1, numberOfBins, colors="#995050", linewidths=5)

   # Style
   ax.set_xlim(-1,numberOfBins); ax.set_ylim(0,max(realValues)+2)
   ax.set_xticklabels(" 123456 ")
   ax.set_xlabel("Groups")
   ax.set_ylabel("Weight/Value")

   plt.show()

def main():
   numberOfBins = int(input("Enter the number of bins: "))
   data = create_resources()
   groups = run_greedy(data,numberOfBins)
   #idealValue,realValues=analysis(data,groups,numberOfBins)
   #visualization(idealValue,realValues,numberOfBins)

if __name__ == "__main__":
    main()