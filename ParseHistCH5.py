import numpy as np
from CH5-DCH.py import HHdist

with open("Data/Compilation1DW/AHHancestors.xyz","r") as f:
	data = f.readlines()

numatoms = 6
xyzcell = numatoms + 3
numancestors = len(data)/9
ancestors = np.zeros((numancestors,6,3))
data = np.array(data)

for i in range(0,len(data)):

	if i%xyzcell == 1:	
		walker = np.zeros((6,3))
	
	if i%xyzcell == 2:
		coord = data[i].split()
		extra = coord.pop(0)
		walker[0][:] = coord
	if i%xyzcell == 3:
		coord = data[i].split()
		extra = coord.pop(0)
		walker[1][:] = coord
	if i%xyzcell == 4:
		coord = data[i].split()
		extra = coord.pop(0)
		walker[2][:] = coord
	if i%xyzcell == 5:
		coord = data[i].split()
		extra = coord.pop(0)
		walker[3][:] = coord
	if i%xyzcell == 6:
		coord = data[i].split()
		extra = coord.pop(0)
		walker[4][:] = coord
	if i%xyzcell == 7:
		coord = data[i].split()
		extra = coord.pop(0)
		walker[5][:] = coord
	if i%xyzcell == 8:
		ind = i/9
		ancestors[ind]=walker
