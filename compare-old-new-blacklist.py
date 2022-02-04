"""


Input
^^^^^
All inputs are currently hard-coded.
- `newFile`: path for generated taxid blacklist csv file ../blacklist-taxId.unique.csv
- `oldFile`: path for generated all taxids blacklist txt file ../Blacklist_version1_all_taxID_YH.txt
- `compareFile`: path for ../compare-new-old-blacklist.txt

Output
^^^^^^
All outputs are currently hard-coded.
- The `compare-new-old-blacklist.txt` is generated.

Usage
^^^^^
- Currently no options available. 
"""
from optparse import OptionParser

__version__="1.0"
__status__ = "Dev"



###############################
def main():

	newFile = "/data/projects/targetdbs/filtered-nt/generated/blacklist-taxId.unique.csv"
	oldFile = "/data/projects/targetdbs/filtered-nt/generated/Blacklist_version1_all_taxID_YH.txt"
	compareFile = "/data/projects/targetdbs/filtered-nt/generated/compare-new-old-blacklist.txt"
	
	oldList = {}
	with open(oldFile, "r") as FR1:
		for line in FR1:
			line = line.strip().split('\t')
			try:
				oldList[line[0]] = line[1]
			except:
				oldList[line[0]] = "NA"

	newList = {}
	i = 0
	with open(newFile, 'r') as FR2: 
		for line in FR2:
			line = line.strip().split(',')
			if not line[0] in oldList:
				with open(compareFile, "w") as FW: 
					FW.write("Newly added taxIds: %s,%s\n" % (line[0],line[1]))
			else:
				i += 1
			newList[line[0]] = 1

	with open(compareFile, "w") as FW: 
		for j in oldList:
			if not j in newList:
				FW.write("Deleted taxIds: %s,%s\n" % (j,oldList[j]))

	print("The number of taxIds included in both old and new black list is:", i)

if __name__ == '__main__':
        main()

