import numpy as np

#Question 1
#Make a NumPy array called array1 from a list [0, 10, 4, 12]. Subtract 20 from array1. What is the result? What is the shape of array1?

def solveQ1():
    
    #create the list
    list1 = [0, 10, 4, 12]

    #convert into array
    array1 = np.array(list1)

    #Substract 20 from array
    array1 = array1 -20
    
    #print result and shape of array
    print('Result:',array1)
    print('Shape:', array1.shape)

#Question 2
#Make a 2D array2 from [0, 10, 4, 12], [1, 20, 3, 41]. 
#Use array restructuring and indexing to create a new array array2_new that is a 2x2 array with values [[4, 12], [1, 20]]. 

def solveQ2():
    
    #create array
    array2 = np.array([[0, 10, 4, 12], [1, 20, 3, 41]])

    #use indexing for new array
    array2_new = np.array([[array2[0, 2], array2[0, 3]], 
                         [array2[1, 0], array2[1, 1]]])

    #print result
    print('new array:')
    print(array2_new)

#Question 3 
#Using array1, 
#create the following array named array3 using hstack() and vstack():

def solveQ3():
    
    #create the lsit array1
    array1 = np.array([0,10,4,12])

    #stack the array 4 times vertically afte stacking it two times horizontally
    array3 = np.vstack([np.hstack((array1, array1)) for _ in range(4) ])
    
    #print out result
    print('Result:')
    print(array3)

#Question4
#Using arange(), make an array called array4a that will contain [-3, 3, 9, 15] and array4b that will contain [-7, -9, -11, -13, -15, -17, -19].

def solveQ4():
    
    #use arange() to produce an arry of numbers between -3 and 15 with a step size of 6
    array4a = np.arange(-3,16,6)

    #printout result
    print('array4a:')
    print(array4a)

    #use arange() to produce an array of numbers between -7 and -19 with a step size of -2
    array4b = np.arange(-7,-20,-2)

    #printout result
    print('array4b:')
    print(array4b)

#Question5():
#Make an array called array5 using linspace() that goes from 0 to 100 with 49 steps. How does this differ from arange()? When might you use one over the other?

def solveQ5():

    #create array using linspace() 
    array5 = np.linspace(0,100,49)

    #printout result
    print('array4b:')
    print(array5)
    
    #differs from arrange() because when using linspace() you specify the steps taken in the intervall and not the step size between the number 
    #In addition the highest number is included when using linspacea() which is not the case with arange()

#Create an array called array6. 
# First, initialize the array with all zeros 
# and then fill its content with appropriate slicing operations so that the following print statements would produce the output displayed in the comments 
# (it’s fine if you want to first doodle out on paper what it might look like before you get started):

def solveQ6():
    
    #initialize array 6 with all zeros with integer as a datatype because per default the zeros function creates an array with floats 
    #which lead to points at the end of the number in the array
    array6 = np.zeros((3, 4), dtype= int )

    #set first row 
    array6[0,:] = [12,3,1,2]

    #set elements [1,2] and [1,3]
    array6[1,2:] = [1,2]

    array6[2,:] = [4,2,3,1]

    #check results
    #searched for a way to compare the whole array in one statement so that the output for (array6[:, 1] ==  [3, 0, 2]) is not [True, True, True]
    #found .all() function
    print(array6[0].tolist() == [12, 3, 1, 2])
    print(array6[1, 0] == 0)
    print((array6[:, 1] ==  [3, 0, 2]).all())
    print((array6[2, :2] == [4, 2]).all())
    print((array6[2, 2:] == [3, 1]).all())
    print((array6[:, 2] == [1, 1, 3]).all())
    print(array6[1, 3] == 2)

    #print result
    print('result:')
    print(array6)

#Question 7 
#Using string parsing, vstack(), and a for loop, create an array named array7 with dimensions of 100x4 
#that contains identical repeating rows of four values taken from: string7 = "1,2,3,4".

def solveQ7():

    #create string7
    string7 = '1,2,3,4'

    #split string by commas and store nummer as an integer in an array
    row = np.array(string7.split(','), dtype = int)

    #create an array in stacking row a 100 times 
    array7 = np.vstack([row for x in range(100)])

    #print result
    print('result:')
    print(array7)
    
    #Check for correct shape
    print(array7.shape)

solveQ7()

