class Person:

   

   def __init__(self, name = 'Uknown', 
                 city = 'Uknown', occupation = 'Uknown', 
                 stats =  {
                    'str': '0',
                    'dex': '0',
                    'con': '0',
                    'int': '0',
                    'wis': '0',
                    'chr': '0'
                 },
                 bio = "Not much is known about this person", 
                 race="Uknown", alignment = "Uknown", 
                 sex = "Uknown", age = "Uknown"):
      self.name = name
      self.city = city
      self.occupation = occupation
      self.stats = stats
      self.bio = bio
      self.race = race
      self.alignment = alignment
      self.sex = sex
      self.age = age

   def copyDict(self, mydict):
      for key in mydict:
         if(mydict[key] == ''):
            continue
         if key in self.stats.keys():
            self.stats[key] = mydict[key]
         else:
            setattr(self, key, mydict[key])


    
        
