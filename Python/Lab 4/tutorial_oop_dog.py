#define class Dog its attributes and its methods
class Dog():
  name = ""
  age = 0
  __breed = None
  def __init__(self, dog_name, dog_age, dog_breed):
    self.name = dog_name
    self.age = dog_age
    self.__breed = dog_breed
    
  def speak(self, sound):
    print(self.name, "says", sound)

  def run(self, speed):
    print(self.name, "runs", speed, "mph")

  def description(self):
    print(self.name, "is a", self.age,  "year old", self.__breed)

  def define_buddy(self, buddy):
    self.buddy = buddy
    buddy.buddy = self


#instanciate scout and print its attributes
scout = Dog("Scout", 2, "Belgian Malinois")
print(scout)
#print(scout.__breed)
print(scout.name)
print(scout.age)

#call methods of scout
scout.speak("woof")
scout.description()

#Question 3:

#instantiate skippy
skippy = Dog("Skippy", 2, "Golden Retriever")

#make skippy and scout buddies
scout.define_buddy(skippy)

#printout skippys description using the fact tht he is a buddy of scout
scout.buddy.description()

