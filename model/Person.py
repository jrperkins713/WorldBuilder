class Person:

   

   def __init__(self, name = 'Unknown', 
                 city = 'Unknown', occupation = 'Unknown', 
                 stats =  {
                    'str': '0',
                    'dex': '0',
                    'con': '0',
                    'int': '0',
                    'wis': '0',
                    'chr': '0'
                 },
                 bio = "Not much is known about this person", 
                 race="Unknown", alignment = "Unknown", 
                 sex = "Unknown", age = "Unknown"):
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


    
        
