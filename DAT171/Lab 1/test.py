
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.sparse import csr_matrix
from matplotlib.collections import LineCollection

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#plt.scatter(coord[:,0],coord[:,1], s = 3, c= 'r')  # Plot the coords as points


lines = LineCollection([[(0,1), (1,1)]])
ax.add_collection(lines)

plt.show()
