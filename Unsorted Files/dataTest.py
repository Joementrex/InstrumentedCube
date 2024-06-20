import numpy as np

data = [[0, -10], [1, 20], [2, 30], [3, 40], [4, 50], [5, 60], [6,70], [7,80], [8,90]]

print(data)

# extract the 2nd element of each list in data
data2 = [x[1] for x in data]
print(data2)
# take the abs of each value
data2 = [abs(x) for x in data2]
# for each data in data2, abs and sum the values in groups of three
data3 = [sum(data2[i:i+3]) for i in range(0, len(data2), 3)]
print(data3)

# make data3 be every 3rd value in data2 starting from the 2nd value
data3 = data2[1::3]
print(data3)

# scale the values in data3 to be between 0 and 1
data3 = [x/1000 for x in data3]

# convert each value in data3 to an rgb value
data4 = [[x, x, x, 1] for x in data3]
print(data4)

# convert to numpy array
data4 = np.array(data4)
print(data4)