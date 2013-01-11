"""
Class which tells a user gossip, eithe specifically or psuedo-randomly 
chosen, depeneding on the input parameters. The class will check whether
The user already knows the fact, i.e. they were in the chatroom when 
the gossip was told. If the user wants to know gossip about another person, 
the class will not gossip about this person. 
"""
from state import State
from database.dbsetup import Database
from database.fact import Fact
import random

class Gossip(State):
    @staticmethod
    def respond(context):
        subject = None

        if context['isAffirmative'] == True:
           #if it's a targeted query, get the subject of the gossip
           if context['specific'] == True:
               subject = context['subject']
        
           query = '''SELECT * FROM facts'''
           db = Database()
           temp_results = db.query(query)

           results = [] 
           #remove results where asker is knower
           for result in temp_results:
               knowers = result[3].split("; ")
               if context['_nick'] not in knowers:
                   results.append(result)
                   
           #if there is no gossip the user doesn't know
           if len(results) == 0:
               db.close_conn()
               responses = ["You already know everything I know!",

                            "I can not believe you enjoy gossip as" \
                            + " much as me, but I do not have any more gossip" \
                            + " to tell you now.",
                            "I think you should go talk to others in this room," \
                            +   " because I am all out of gossip.", 
                            "Hmmm... well, I don't really know anything right now...."]

               rand_ndx = random.randint(0, len(responses) - 1)

               return responses[rand_ndx]

           #choices for leading off gossip
           prefix = ["Did you know that ",
                     "I heard that ", 
                     "A little birdy told me that ", 
                     "Someone told me that ", 
                     "You didn't hear it from me, but I heard that ", 
                     "Don't tell anyone that "]
        
           gossip = []

           #if it's a speicifc query
           if subject != None:
               #checks if user is in the room
               if State.users != None and subject in State.users:
                   db.close_conn()
                   return "Oh, " + subject + " is just so nice... nothing to say about them!"
               else:
                   specific_results = []
                   #generate list of speciifc queries metioning the subject
                   for result in results:
                       if subject in result:
                           specific_results.append(result)
                       #check the message for occurances of the user
                       else: 
                           tokens = result[1].split(" ")
                           for token in tokens:
                               if subject.lower() == token.lower():
                                   specific_results.append(result)
                   #if you can't find any results
                   if len(specific_results) == 0:
                       db.close_conn()
                       return "You already know everything I know about " + subject + "!"
                   #randomly select a specific fact
                   rand_ndx = random.randint(0, len(specific_results)-1)            
                   gossip = specific_results[rand_ndx]                
           else: #randomly grab facts
               rand_ndx = random.randint(0, len(results)-1)            
               gossip = results[rand_ndx]            


           #select prefix
           rand_ndx2 = random.randint(0, len(prefix)-1)        

           response = ""
           #generate response
           
           if len(gossip[2]) == 0 or gossip[2] == None:
               response = prefix[rand_ndx2] + gossip[0] + " " + gossip[1] + "!"  
           else: 
               response = prefix[rand_ndx2] + gossip[2] + " told "  + \
                   gossip[0] + ", \"" + gossip[1] + "\"!"
           #if you didn't find any random facts
           if len(gossip) == 0:
               db.close_conn()
               return "Hmmm... well, I don't really know anything right now...."
           else:
               #update the knowers to include the user asking for gossip
               knowers = gossip[3].split("; ") 
               knowers.append(context['_nick'])
               print knowers
               
               #add all users in the room to the knowers
               if State.users != None:
                   for user in State.users:
                       knowers.append( user)

               knowers = set(knowers)
               print knowers
               knowers = "; ".join(knowers)
               update_statement = "UPDATE facts SET knowers = \'" + knowers + \
                                  "\' WHERE author= \'" + gossip[0] + \
                                  "\' AND msg= \'" + gossip[1] + \
                                  "\' AND recipient= \'" + gossip[2] + "\';" 
                                  
               db.update(update_statement)
               
               db.close_conn()
               return response
        else:
            responses = ["Too bad... I had something really juicy!",
                         "No gossip? Guess I'll have to go tell someone else this big secret.",
                         "Do not worry, I will not tell anyone that you do not like to gossip..."]

            rand_ndx = random.randint(0, len(responses) - 1)
            return responses[rand_ndx]

State.register(Gossip, True)
