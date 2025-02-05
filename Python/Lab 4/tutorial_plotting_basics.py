import matplotlib.pyplot as plt
import numpy as np

#first plot 
x = [1,2,3,4]  # x data vector (as a list)
y = [1,4,9,16] # y data vector (as a list)
plt.clf()      # clear any existing plot
plt.plot(x,y)  # write the data onto the figure buffer
plt.show()     # show the figure

#second plot 
a = np.array([[1,2,3,4],[1,4,9,16]])
plt.clf()
plt.plot(a)
plt.show()

#if you plot this you get 4 linear plots in the same figure.
#the array is interpreted such that the values in the first row are assigned to the x values zero
#the values in the second row i are the x value 1
#the points with the same column indices are connected and the result is a linear function with start points from the first and end points from the second row

#third plot
a = np.array([[1,2,3,4],[1,4,9,16]])
x = a[0,:] #index from a to get [1,2,3,4]
y = a[1,:] #index from a to get [1,4,9,16]
plt.title("First plot!")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(x,x)
plt.plot(x,y)
plt.show()

#fourth plot with subplot
plt.clf()
plt.subplot(211)
plt.plot([1,2,3,4],[1,4,9,16])
plt.subplot(212)
plt.plot([1,2,3,4],[4,2,1,6])
plt.show()

