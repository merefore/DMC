import numpy as np

with open("4deut_ancestors.xyz","r") as f:
	data = f.readlines()

######    WHICH DISTANCE DO YOU WANT?
##HH/D     1
##DD       2
##HD      3
parameter = 1	
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
	
histPile = []

#### DIFFERENT DISTANCE CODES
if parameter == 1: #HH/D
	for i in range(0,len(ancestors)):
		HHdist = np.zeros(10)
		xh = np.zeros(5)
		yh = np.zeros(5)
		zh = np.zeros(5)
		
		for j in range(1,6):
			xh[j-1] = ancestors[i,j,0]
			yh[j-1] = ancestors[i,j,1]
			zh[j-1] = ancestors[i,j,2]
			
		b=0
		
		for k in range(0,4):
			for m in range(k+1,5):
				HHdist[b] = np.sqrt((xh[k]-xh[m])**2+(yh[k]-yh[m])**2+(zh[k]-zh[m])**2)
				histPile.append(HHdist[b])
				b+=1

if parameter == 2: #DD
	for i in range(0,len(ancestors)):
		HHdist = np.zeros(6)
		xh = np.zeros(4)
		yh = np.zeros(4)
		zh = np.zeros(4)
		
		for j in range(1,5):
			xh[j-1] = ancestors[i,j,0]
			yh[j-1] = ancestors[i,j,1]
			zh[j-1] = ancestors[i,j,2]
		b=0
		
		for k in range(0,3):
			for m in range(k+1,4):
				HHdist[b] = np.sqrt((xh[k]-xh[m])**2+(yh[k]-yh[m])**2+(zh[k]-zh[m])**2)
				histPile.append(HHdist[b])
				b+=1
	
if parameter == 3: #HD
	for i in range(0,len(ancestors)):
		HHdist = np.zeros(4)
		xh = np.zeros(5)
		yh = np.zeros(5)
		zh = np.zeros(5)
		
		for j in range(1,5):
			xh[j-1] = ancestors[i,j,0]
			yh[j-1] = ancestors[i,j,1]
			zh[j-1] = ancestors[i,j,2]
		b=0
		
		for m in range(0,4):
			HHdist[b] = np.sqrt((xh[4]-xh[m])**2+(yh[4]-yh[m])**2+(zh[4]-zh[m])**2)
			histPile.append(HHdist[b])
			b+=1

histPile = np.array(histPile) 


standard_bins = np.arange(1.0,4.8,0.05)	
#totalHIST, bin_edges = np.histogram(histPile,bins=standard_bins)

totalHIST, bin_edges = np.histogram(histPile, bins=75)

width1 = bin_edges[1]-bin_edges[0]
newNhist = totalHIST/(np.sum(totalHIST)*width1)
bin_edges = np.delete(bin_edges,len(bin_edges)-1)

print 'BIN EDGES'
for entry in bin_edges:
	print '%f' % entry
print '\n\nHIST VALUES'
for entry in newNhist:
	print '%f' % entry
