Frederik Simon 

PID: 10310072

## Lab 1 Tutorial 1 completed 

To complete the Lab 1 Tutorial 1, I installed python directly from python.org and also installed the python extension for Microsoft Visual Code. I tried to execute my first program using the 'python3' command wich I had used on my previous devices to run python, but it did not work for me. After researching with the help of the internet, I discovered that there is no need to use the 'python3' command. I can just use the 'python' command which automatically points to Python 3.

## Lab 1 Tutorial 2 completed 

In the Tutorial 2 I mostly learned about List Slicing, List Comprehensions, strings in python and looping over lists. I had backround knowledge of how to initialize and modify list and it was interesting to learn how easily you can access multiple entries in a lists simutanously and manipulate them element wise. From the tutorial section about strings, the most memmorable part for me was learning about the split operation of strings, which makes it easy to break a string into parts based on a delimiter. Additionally, knowing that the python interpreter sets special variables such as '\_\_name\_\_', which can be used to determine if the module was imported from another module, could also prove to be very powerful in the future.

## Lab 1 Tutorial 3 completed 

The content of Tutorial 3 was an introduction in the NUMPY package, which is an numerical computation package. I mostly learned about different ways to initialize new arrays for example from a list or as an array full of zeros, restructuring and resizing them and also how to slice and use the indexing notation.
After reading and trying out the contents of the tutorial I solved the Questions that were given to test the knowledge gained by the Tutorials two and three.

__Questions 1__ and __2__ were simple list to array conversion and indexing

In the proccess of solving __Question 3__ I had some sytax problems because the cascaded stacking required a precise placing of brackets, where there has to be a double bracket around the argument of the first horizontal stacking:

```python 
array3 = np.vstack([np.hstack((array1, array1)) for _ in range(4) ])
```


The __Questions 4 and 5__ asked you to explore the difference between the methods 'arange()' and 'linspace()' which both initialize an array. The difference between them is that you specify the step size for 'arange()' and for linspace you specify the amount of steps taken in the intervall. In Addtion, the specified upper boundary of the intervall is included in the array when using 'linspace()', but not when using 'arange()'. Furthermore, what I learned is that if using 'arange()' with declining negative numbers, the step size also has to be specified as a negative number, regardless if the intervall implies a negative stepping direction.

For __Question 6__ I wrote down my array and then set the nonzero values to the correct values.
[Bild]

To solve __Question 7__ I split the string by the commas and specified the datatype as integer to avoid the array being initialized with floats or strings:
```python
row = np.array(string7.split(','), dtype = int)
```

At a last step I stacked the array a hundred times to obtain the desired result.



## Lab 1 Challenge 1 completed 

The objective of the __Challenge 1__ in the Lab 1 was to get familiar with working on and with lists, loops, if statements and logic controls, Error Handling, Assertions and Functions. First the goal was to understand the concept and then to apply the gained knowledge in several tasks.

For the __Exercises 0.3__ two lists should be initialized with different datatypes as content, then the diffferent lists should be manipulated and
joint using different methods. In addition to that, I checked if I have initialized the lists the right way and if the numbers in the lists have the right datatype. One thing, I was reminded of in this exercise is that you need to be careful how to copy your list:
```python
list_1_copy = list_1 #list_1_copy is just a pointer to list_1
list_1_copy = list_1[:] #actually copies the list
```
For the last two Questions, you had to find a way to append new data to an existing list that has a fixed length. I did this with the help of slicing and defining a length to keep of the existing list, which depends on the size of the new data and the already existing list. The kept data is copied in the beginning of the already existing list and the new is appended after. For the edge cases, when a different datatype than a list is passed to the function and when an empty list is passed, I implemented if statements that return an Error message or an empty list respectively. 

To complete the __Exercises 1.4__ you have to create a lists with commands as strings and loop over list printing the elements to the console using both a for and a while loop. Clearly, the for loop is the most convinient to use as you can easily loop over lists and other items. When using a while loop you often have to define a variable that controls how often the loop should be executed. 
Additionally, I learned the difference between using 'in' and '==' when comparing strings. Whereas 'in' compares the whole string to a second string, '==' compares the string character by character to another string. When you use the escape character '\' in a string it introduces a special character after it, thus the last logic statement evaluates to 'False'.
Using this knowledge I solved the last excercise, by looping over a given list until the string "SUCCESS" occurs in one of the entries and then braking the loop and printing "This worked!".

The goal of the __Exercises 2.2__ are to get familiar with how to handle Errors and also catch them and make your code robust. To solve the Exercise 5, the function tries to decode the input variable from a byte array to a string, if this fails and a UnicodeDecodeError arises, the function returns an empty string.






