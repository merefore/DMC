import numpy as np
import glob

filenames = glob.glob('3deut_ancestors*.xyz')
data = []
for entry in filenames:
	with open(entry,"r") as f:
		data = data + f.readlines()

######    WHICH DISTANCE DO YOU WANT?
##HH/D     1
##DD       2
##HD       3
##HH       4
parameter = 4
numatoms = 6
xyzcell = numatoms + 3
data = np.array(data)
numancestors = (len(data)/9)
ancestors = np.zeros((numancestors,6,3))

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
	
HDhistPile = []
DDhistPile = [] 
HHhistPile = []
ancestordist = np.zeros((len(ancestors),10))

#### DIFFERENT DISTANCE CODES
# the ancestor dist file goes [HD1,HD2,HD3,HD4,HD5,HD6,DD1,DD2,DD3,HH] for each ancestor i

for i in range(int(len(ancestors)*0.33),len(ancestors)):
#HD
	HDdist = 0
	xh = np.zeros(5)
	yh = np.zeros(5)
	zh = np.zeros(5)
	
	for j in xrange(1,6):
		xh[j-1] = ancestors[i,j,0]
		yh[j-1] = ancestors[i,j,1]
		zh[j-1] = ancestors[i,j,2]
	b=0
	for k in xrange(3,5):
		for m in xrange(0,3):
			HDdist = np.sqrt((xh[k]-xh[m])**2+(yh[k]-yh[m])**2+(zh[k]-zh[m])**2)
			ancestordist[i,b] = HDdist
			HDhistPile.append(HDdist)			
			b+=1
#DD
	DDdist = 0
	xh = np.zeros(3)
	yh = np.zeros(3)
	zh = np.zeros(3)
	
	for j in xrange(1,4):
		xh[j-1] = ancestors[i,j,0]
		yh[j-1] = ancestors[i,j,1]
		zh[j-1] = ancestors[i,j,2]
	
	for k in xrange(0,2):
		for m in xrange(k+1,3):
			DDdist = np.sqrt((xh[k]-xh[m])**2+(yh[k]-yh[m])**2+(zh[k]-zh[m])**2)
			ancestordist[i,b] = DDdist
			DDhistPile.append(DDdist)
			b+=1

#HH
	HHdist = 0
	xh = np.zeros(5)
	yh = np.zeros(5)
	zh = np.zeros(5)
	
	for j in xrange(1,6):
		xh[j-1] = ancestors[i,j,0]
		yh[j-1] = ancestors[i,j,1]
		zh[j-1] = ancestors[i,j,2]
	
	HHdist = np.sqrt((xh[3]-xh[4])**2+(yh[3]-yh[4])**2+(zh[3]-zh[4])**2)
	ancestordist[i,b] = HHdist
	HHhistPile.append(HHdist)
	b+=1

	HHbins = np.append(np.arange(0.5,2.75,0.015),2.75)
	conPiles = [[]]
	for i in xrange(150):
		conPiles.append([])
		
	for x in xrange(0,len(HHbins)-1):
		if HHbins[x] <= HHdist < HHbins[x+1]:
			# for j in range(0,6):
				# HDhistPile.append(ancestordist[i,j])
			for l in xrange(6,9):
				conPiles[x].append(ancestordist[i,l])

conPiles = np.array(conPiles)

conHists = []

standard_bins = np.arange(0.5,2.75,0.015)
for i in xrange(150):
	totalHist, bin_edges = np.histogram(conPiles[i], bins=standard_bins)
	width1 = bin_edges[1]-bin_edges[0]
	newHist = totalHist/(np.sum(totalHist)*width1)
	conHists[i].append(totalHist)
			
# HHhistPile = np.array(HHhistPile)*0.529177
# HDhistPile = np.array(HDhistPile)*0.529177
# DDhistPile = np.array(DDhistPile)*0.529177

	
#totalHIST, bin_edges = np.histogram(histPile,bins=standard_bins)

# totalHHhist, bin_edges = np.histogram(HHhistPile, bins=standard_bins)
# totalHDhist, bin_edges = np.histogram(HDhistPile, bins=standard_bins)
# totalDDhist, bin_edges = np.histogram(DDhistPile, bins=standard_bins)

# width1 = bin_edges[1]-bin_edges[0]
# newHHhist = totalHHhist/(np.sum(totalHHhist)*width1)
# newHDhist = totalHHhist/(np.sum(totalHDhist)*width1)
# newDDhist = totalHHhist/(np.sum(totalDDhist)*width1)
# bin_edges = np.delete(bin_edges,len(bin_edges)-1)

# print 'BIN EDGES'
# for entry in bin_edges:
	# print '%f' % entry
# print '\n\nHIST VALUES'
# for entry in newNhist:
	# print '%f' % entry