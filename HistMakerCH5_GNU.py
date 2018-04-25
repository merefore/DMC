import matplotlib.pyplot as mpl
import numpy as np

# data = [line.rstrip('\n') for line in open('histDataGS.txt')]

with open('Data/Compilation1DW/AHHhistdata.txt') as f:
    data1 = np.array(f.readlines())
	
data1 = data1.astype(float)

with open('Data/Compilation1DW/BHHhistdata.txt') as f:
    data2 = np.array(f.readlines())
	
data2 = data2.astype(float)

with open('Data/Compilation1DW/DHHhistdata.txt') as f:
    data3 = np.array(f.readlines())
	
data3 = data3.astype(float)

with open('Data/Compilation1DW/DHHbinedges.txt') as f:
	bin_edges = np.array(f.readlines())


data = data1 + data2 + data3	
bin_edges = bin_edges.astype(float)
bin_edges = bin_edges * 0.52917725

width1 = bin_edges[1]-bin_edges[0]

printfile = open("HHdistGNU.txt", "a+")

for x in range(0,len(data)):
	printfile.write("%f %f\n" % (bin_edges[x],data[x]))

printfile.close()

# mpl.bar(bin_edges,data,width=width1)
# mpl.show()
