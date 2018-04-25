import timeit
import math
import itertools
import random
import numpy as np
# import matplotlib.pyplot as mpl
import CH5pot

START = timeit.default_timer()

n0 = 20000 #number of initial walkers
dtau = 10 #time step
m1 = 21894.687 #C
m2 = 1837.515 #H
m3 = 3671.571 #D
sigma1 = np.sqrt(dtau / m1)
sigma2 = np.sqrt(dtau / m2)
sigma3 = np.sqrt(dtau / m3)
cycles = 10000
alpha = 0.5 / dtau

def V(whereUat): #-----------our potential function
	v = np.zeros(len(whereUat))
	emin = -40.65276470207075 
	v = CH5pot.mycalcpot(whereUat,len(whereUat))
	v = np.array(v)
	return v # must return a 1D numpy array
	
def avg(potentials, init): #-------------our vref function
	potTotal = potentials.sum()
	vref = potTotal / float(len(potentials)) - alpha*(len(potentials)-init)/float(init)
	return vref
	
def pcalc(potentials, vref, dtau): #------------to calculate pvalues
	a = -(potentials - vref) * dtau
	pvalues = np.exp(a)
	return pvalues
	
def Fate(whereUat,whereUfrom,potentials,pvalues): #--------will return our new collection of walkers 
	positions2 = []
	potentials2 = []
	elders2 = []

	whole = pvalues.astype(int)
	frac = pvalues - whole
	Nr = np.random.random(len(whereUat))
	Nr2 = np.random.random(len(whereUat))

	for i in range(0,len(whole)):
		if potentials[i] > 0:
			if whole[i] != 0:
				for h in range(0,whole[i]):
					positions2.append(whereUat[i])
					potentials2.append(potentials[i])
					elders2.append(whereUfrom[i])
			if Nr[i] < frac[i]:
				positions2.append(whereUat[i])
				potentials2.append(potentials[i])
				elders2.append(whereUfrom[i])
	
	positions2 = np.array(positions2)
	potentials2 = np.array(potentials2)
	elders2 = np.array(elders2)
	return positions2,potentials2,elders2
	
def CHAvgDistDW(whereUfrom, ancestors, histPile): #--------calculating DW for average CH distance in molecule
	CHdist = np.zeros(5)
	xh = np.zeros(5)
	yh = np.zeros(5)
	zh = np.zeros(5)
	
	for i in whereUfrom:
		xc = ancestors[i,0,0]
		yc = ancestors[i,0,1]
		zc = ancestors[i,0,2]
		for j in range(1,6):
			xh[j-1] = ancestors[i,j,0]
			yh[j-1] = ancestors[i,j,1]
			zh[j-1] = ancestors[i,j,2]
		
		for k in range(0,5):
			CHdist[k] = np.sqrt((xc-xh[k])**2+(yc-yh[k])**2+(zc-zh[k])**2)		
			histPile.append(CHdist[k])
			
	return histPile

#Initialize Walkers
beginning = np.array([[0.000000000000000, 0.000000000000000, 0.3869923621587414],
[0.000000000000000, 0.000000000000000, -1.810066283748844],
[1.797239666982623, 0.000000000000000,   1.381637275550612],
[-1.797239666982623, 0.000000000000000, 1.381637275550612],
[0.000000000000000, -1.895858229423645, -0.6415748897955779],
[0.000000000000000, 1.895858229423645, -0.6415748897955779]])

whereUat = np.zeros((n0,beginning.shape[0],beginning.shape[1]))

for i in range(0,n0):
        whereUat[i] = beginning * 1.1
		
# potentials = V(whereUat)	

#------    FILENAMES   ---------
#######                                          #########
#######                                          #########
#######                                          #########
fileEnergy = open("3deut_energies.txt", "a+")
fileXYZ = open("3deut_ancestors.xyz", "a+")
fileHistData = open("3deut_histdata.txt", "a+")
fileBinEdges = open("3deut_binedges.txt", "a+")
timestep = 0
energies = []
population = []
ancestorPile = []
histPile = []

#BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM BEGIN PROGRAM

for c in range(0,cycles):    
	# positionsOld = whereUat
	# potentialsOld = potentials

	if timestep%500 == 0:
		ancestors = whereUat
		whereUfrom = np.arange(0,len(whereUat)) #initialize the "index array", which will reference indexes in "ancestors"
		
	# Create Random Displacements # (Remember the mass!)
	displace = np.random.normal(0,sigma2,whereUat.shape)
	for i in range(0,len(displace)): 
		displace[i,0,:] = np.random.normal(0,sigma1,(1,3))
		displace[i,1,:] = np.random.normal(0,sigma3,(1,3))
		displace[i,2,:] = np.random.normal(0,sigma3,(1,3))
		displace[i,3,:] = np.random.normal(0,sigma3,(1,3))
	
	# Displace the Walkers #
	whereUat = whereUat + displace
	
	# Calculate the Potential #
	potentials = V(whereUat) #using my function V 
	
	# Take Vref #
	vref = avg(potentials, n0) #umf avg
	energies.append(vref)
	fileEnergy.write("%f\n" % vref)
	population.append(len(whereUat))
	
	# Calculate PValues #
	pvalues = pcalc(potentials, vref, dtau) #umf pcalc
	whereUat,potentials,whereUfrom = Fate(whereUat,whereUfrom,potentials,pvalues) #umf Fate
	
	if timestep%500 == 0:
		print vref, ", ", timestep, ", ", len(whereUat)
	
	# Desc. Weighting #
	# avgCH distance #
	if 0 < timestep%500 < 50 and timestep > 4000:
		histPile = CHAvgDistDW(whereUfrom, ancestors, histPile) #umf CHAvgDistDW
	
	if timestep%500 == 50:
		for i in whereUfrom:
			ancestorPile.append(ancestors[i])

	timestep += 1
ancestorPile = np.array(ancestorPile)
histPile = np.array(histPile) 

standard_bins = np.arange(1.6,3.0,0.028)	
totalHIST, bin_edges = np.histogram(histPile,bins=standard_bins)
totalHIST = totalHIST/5

#HIST, bin_edges = np.histogram(histPile, bins=75)

width1 = bin_edges[1]-bin_edges[0]
newNhist = totalHIST/(np.sum(totalHIST)*width1)
bin_edges = np.delete(bin_edges,len(bin_edges)-1)
	
for entry in newNhist:
	fileHistData.write("%f\n" % entry)	
for entry in bin_edges:
	fileBinEdges.write("%f\n" % entry)
	

b=0
convert = 0.52917725
for item in ancestors: #-----------for jmol xyz file
	fileXYZ.write("6\n")
	fileXYZ.write("CH5+ coordinates         ")
	fileXYZ.write("%i\n" % b)
	fileXYZ.write("C       %f       %f       %f\n" % (item[0,0]*convert, item[0,1]*convert, item[0,2]*convert))
	fileXYZ.write("D       %f       %f       %f\n" % (item[1,0]*convert, item[1,1]*convert, item[1,2]*convert))
	fileXYZ.write("D       %f       %f       %f\n" % (item[2,0]*convert, item[2,1]*convert, item[2,2]*convert))
	fileXYZ.write("D       %f       %f       %f\n" % (item[3,0]*convert, item[3,1]*convert, item[3,2]*convert))
	fileXYZ.write("H       %f       %f       %f\n" % (item[4,0]*convert, item[4,1]*convert, item[4,2]*convert))
	fileXYZ.write("H       %f       %f       %f\n\n" % (item[5,0]*convert, item[5,1]*convert, item[5,2]*convert))
	b+=1

fileEnergy.close()
fileXYZ.close()
fileHistData.close()
fileBinEdges.close()

STOP = timeit.default_timer()
print "Time to calculate: ", STOP - START, " seconds"
avgEn =np.average(energies)
print "Energy: ", avgEn

# --------Histogram Bar Graph
# mpl.bar(bin_edges,newNhist,width=width1)
# mpl.show()

# --------Histogram (not bar)
# mpl.hist(positionPile, bins=100)
# mpl.show()

# --------Energy and Population Tracking
# t = range(0,cycles)
# mpl.subplot(211)	
# mpl.plot(t, energies)
# mpl.subplot(212)
# mpl.plot(t, population, 'r')
# mpl.show()
