import matplotlib.pyplot as mpl
import numpy as np

# data = [line.rstrip('\n') for line in open('histDataGS.txt')]

with open('HHhistdata.txt') as f:
    data1 = np.array(f.readlines())
	
data1 = data1.astype(float)

with open('HHbinedges.txt') as f:
	bin_edges = np.array(f.readlines())

bin_edges = bin_edges.astype(float)
bin_edges = bin_edges * 0.52917725

width1 = bin_edges[1]-bin_edges[0]

mpl.bar(bin_edges,data1,width=width1)
mpl.show()
