import pylab as plt
import numpy as np

X = np.linspace(0,2,1000)
Y = X**2 + np.random.random(X.shape)

plt.ion()
graph = plt.plot(X,Y)[0]
# create bar graph
bargraph = plt.bar(X,Y)

while True:
    Y = X**2 + np.random.random(X.shape)
    graph.set_ydata(Y)
    # update bar graph
    for i, b in enumerate(bargraph):
        b.set_height(Y[i])
        
    plt.draw()
    plt.pause(0.01)