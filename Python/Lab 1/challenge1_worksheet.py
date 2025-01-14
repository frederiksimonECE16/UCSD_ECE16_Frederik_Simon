#0.3 Exercises

#1. Create a list called "list_1" containing the ints (integers) 1-10.
list_1 = [1,2,3,4,5,6,7,8,9,10]

#check if the datatype is integer
for elements in list_1:
    print(type(elements) == int)

#2. Create a list "list_2" containing 11-20 as floats.
list_2 = [11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0]

#check id datatype is float 
for elements in list_2:
    print(type(elements)== float)

#update list_1 with the help of slicing 
list_1[:3] = ["one", "two", "three"]

#print list_1
print("list_1: ", list_1)

#4. CreaCreate a tuple containing the words "eleven", "twelve" and "thirteen"
tup = ("eleven","twelve", "thirteen")

#Assign it to the first three elements from 2
list_2[0:3] = tup

#print list_2
print("list_2: ", list_2)

#5. Join the two lists 
#use the extend() method 
joint_1 = list_1[:]
joint_1.extend(list_2)

#use the"+" operator
joint_2 =  list_1 + list_2

#print the result 
print("joint_1: ",joint_1)
print("joint_2: ",joint_2)

#6. 
def list_shift(base_list, new_data):
    
    #check how much entrys should be kept 
    length_to_keep = len(base_list) - len(new_data)

    #take input list base_list and copy the data that should be kept and the beginning of the base_list
    base_list[:length_to_keep] = base_list[-length_to_keep:]
    
    #copy the list new_data to the end of the base_list
    base_list[len(base_list)-len(new_data):] = new_data

    
    return base_list

fixed_length_list = [1,2,3,4]
new_data = [5,6,7]
#print(list_shift(fixed_length_list, new_data))


def list_shift_bonus(base_list, new_data):
    
    #if the argument passed to the function are not of the type list the function will not work as intended, therefore we return an error message.
    if type(base_list) is not list or type(new_data) is not list:
        print('Error: Arguments are not lists.')
        return


    #If the base_list is empty the fixed length is zero. Therefore when the new data is added with the help of slicing, it violates the fixed length rule.
    #Thus a if loop is implemented to just return the base_list without operating on it.
    if len(base_list) == 0:
        return base_list
    
    #check how much entrys should be kept. Bonus: Value should not get negative. The minimum value is 0, therefore you can do an if else loop
    # and set the value to 0 if the subtraction results in a negative number or you could take the maximum value from the substraction and 0. 
    length_to_keep = max(0, len(base_list) - len(new_data))
    

    #take input list base_list and copy the data that should be kept and the beginning of the base_list
    base_list[:length_to_keep] = base_list[-length_to_keep:]
    
    #copy the list new_data to the end of the base_list
    base_list[len(base_list)-len(new_data):] = new_data

    
    return base_list

print(list_shift_bonus(fixed_length_list, new_data))

#1.4 Exercises
#1. Create list of commands
command_list = ["STATUS", "ADD", "COMMIT", "PUSH", "PULL", "BRANCH", "MERGE"]

#2. Create a for loop that loops over each command and print it
for command in command_list:
    print(command)

#3. Create a while loop that does the same #
i = 0 
while i < len(command_list):
    print(command_list[i])
    i += 1

#4. Create a seperate list of strings 
seperate_list = ["PUSH FAILED", "BANANAS", "PUSH SUCCESS", "APPLES"]

#5. Assign the value "SUCCESS" to a variable called text
text = "SUCCESS"

#6. Test the logic statements 

print ("SUCCESS" in "SUCCESS")
print("SUCCESS" in "ijoisafjoijiojSUCCESS")
print("SUCCESS" == "ijoisafjoijiojSUCCESS")
print("SUCCESS" == text)
print("finish" in "ijoisafjoijioj\finish")

#if you use the 'in' operator it compares the whole string
#if you use the '==' operator it compares chracter by character

#7. Make a for loop that loops over the list from step 4.
# Print each word unless it contains the string from step 5, in which case you should exit the loop and print: "This worked!"

#loop over entries in seperate_list 
for entry in seperate_list:
    
    #check if the entries contain the string saved in text
    if text in entry:
        print("This worked!")
        break #exit loop
    else:
        print(entry)


#2.2 Exercises 
#1.Create a string containing my first name
name = "frederik"

#2. encode the string to a byte array
byte_name = name.encode('utf-8') 

#3. Append a non-utf-8 character
byte_name_bad = byte_name + b'\xef'

#4. Attempt to decode byte_name_bad back to a string using .decode()
#byte_name_bad.decode()
#Error: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xef in position 8: unexpected end of data

#5. Create a try-except clause for decoding byte types. 
#If there is a decoding error, set the return string to an empty string.

def decode_byte_types(byte_to_decode):
    try:         
        #return decoded string if there is no error
        return byte_to_decode.decode()

    #if there is a UnicodeDecodeError return an empty string
    except UnicodeDecodeError:
        return ""

print("function with byte_name_bad as input:", decode_byte_types(byte_name_bad))
print("function with byte_name as input:",decode_byte_types(byte_name))

















