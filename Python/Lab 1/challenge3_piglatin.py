from spellchecker import SpellChecker
spell = SpellChecker()

#define a vowel array
vowel = "aeiouAEIOU"
punctuation ="!?.:"

#translate function for each individual word
def translate(input_string : str):
    
    #initialize counting variable for while and for loop
    i = 0
    j= 0

    #create empty strings for copying the first characters and punctuations to the back
    copy_string=""
    copy_punctuation = ""  

    #create a boolean to store if the string starts with an y 
    y_start = False
    
    #check if the string starts with an y 
    if input_string[0] in "yY":
        y_start = True
        #print("set True")

    #if word starts with a vowel append "yay" and return
    if input_string[0] in vowel:
       
        #append the punctuation
        for char in input_string:
        
            #print("executed")

            #loop over string and store the punctuations in copy_punctuations 
            if char in punctuation:
                copy_punctuation += input_string[j]
                input_string = input_string[:j] + input_string[j+1:]
            
            j += 1
       
        #append yay and punctuations
        input_string += "yay" + copy_punctuation
        
        
        return input_string
        
    #while there are consonants at he beginning store and remove them
    while input_string[i] not in vowel:
        
        #check if the caracter is a 'y' and if its followed by a 'e' and therefore a vowel
        if input_string[i] == "y" and input_string[i+1] == "e":
            break
           
        #print("loop executed") 

        #check if there is a 'Q' followed by a 'u'
        if input_string[i] in "qQ" and input_string[i+1] == "u":
            copy_string += input_string[i]
            copy_string += input_string[i+1]
            input_string = input_string[i+2:]
        else:
            copy_string += input_string[i]
            input_string = input_string[i+1:]

        #print(input_string)

   
    #append the punctuation    
    for char in input_string:
        
        #print("executed")
        
        if char in punctuation:
            copy_punctuation += input_string[j]
            input_string = input_string[:j] + input_string[j+1:]
        j += 1


    #if the word starts with y add 'ey' if it does not add 'ay'
    if y_start == False:
        input_string = input_string + copy_string + "ay" + copy_punctuation
    elif y_start == True:
            input_string = input_string + copy_string + "ey" + copy_punctuation
    
    return input_string


def english_to_pig_latin(input_string : str):
         
    #calling the translate function for each hyphenated word 
    if "-" in input_string:
        
        #split the string by '-'
        split_list = input_string.split("-")
        
        #print(split_list)
        
        #add the translated words with an "-" in the middle
        #variable for tracking entries
        x=0

        #set input string 0
        input_string = ""
        
        for entries in split_list:
            
            #do not print "-" before the first word
            if x != 0:
                input_string += "-"
            
            input_string += translate(entries)
            x += 1
    
    #or calling the translate function for a single word
    else:
        input_string = translate(input_string)
     
    return input_string


def pig_latin_to_english_translate(pig_latin_string: str):

    #create a bool to track if the word starts with an y
    y_start = False
    
    #create an empty string to catch the punctuations
    copy_punctuation =""
    
    #record and delete the punctuations from the back, that the dictionary works
    while pig_latin_string[-1:] in punctuation:
        
        copy_punctuation += pig_latin_string[-1]
        pig_latin_string = pig_latin_string[:-1]
    
    #delete "ay" and "ey"at the end 
    if pig_latin_string[-2:] == "ay":
        
        #delete last to characters
        pig_latin_string= pig_latin_string[:-2]
        #print(pig_latin_string)

    elif pig_latin_string[-2:] == "ey":

        #print("executed")
        #delete last to characters
        pig_latin_string= pig_latin_string[:-2]

        #set boolean y_start to True because there is an ey at the end
        y_start = True

    #for english words that start with y shift the letters to the start until it starts again with a y
    if y_start == True:
        
        while pig_latin_string[0] not in "yY":
            pig_latin_string = pig_latin_string[-1:] + pig_latin_string[:-1]
            #print(pig_latin_string)

    #for other words shift the letters to the start until the word can be found in the dictionary       
    else:

        pig_latin_string = pig_latin_string[-1:] + pig_latin_string[:-1]
        #initialize variable that prevents the loop from endless execution
        i = 0
        while spell.correction(pig_latin_string) == None:
            
            #if clause to prevent endless execution
            if i> 10:
                break
            
            #print("loop")

            pig_latin_string = pig_latin_string[-1:] + pig_latin_string[:-1]
            i += 1

        
        pig_latin_string = spell.correction(pig_latin_string)
        
    pig_latin_string += copy_punctuation
    
    return(pig_latin_string)

def pig_latin_to_english(pig_latin: str):

    if "-" in pig_latin:
        
        #split the string by '-'
        split_list = pig_latin.split("-")
        
        #print(split_list)
        
        #add the translated words with an "-" in the middle
        #variable for tracking entries
        x=0

        #set input string 0
        pig_latin = ""
        
        for entries in split_list:
            
            #do not print "-" before the first word
            if x != 0:
                pig_latin += "-"
            
            pig_latin += pig_latin_to_english_translate(entries)
            x += 1

        #or calling the translate function for a single word
    else:
        pig_latin = pig_latin_to_english_translate(pig_latin)
     
    return pig_latin  


#test = "Yttrium"
#print(english_to_pig_latin(test))
#print(pig_latin_to_english("ustn’tMay"))

test_list = ['Quotient','Mustn\'t','Yellow', 'Honest', 'Thursday', 'Christmas', 
             'Alliteration', 'Information', 'Education', 'Fish', 'Numbers!', 'Toyota!',
             'Mother-in-law', 'Laps', 'Slap', 'August', 'empty-handed', 'Ice-cream',
             'Years', 'Yawn', 'Yard', 'Quiet', 'Quack', 'Yttrium', 'Up-to-date']

for i, word in enumerate(test_list):
    out1 = english_to_pig_latin(word)  
    out2 = pig_latin_to_english(out1)
    print(i+1, 'inputted word:', word)
    print(i+1, 'english -> p-latin:', out1)
    print(i+1, 'p-latin -> english:', out2)