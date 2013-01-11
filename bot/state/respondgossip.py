from gossip import Gossip
from state import State
from database.dbsetup import Database
class RespondGossip(Gossip):
    @staticmethod
    def recognize(msg):
        tell_me_gossip = ["gossip", "secret"]
        keywords = ["tell", "me" , "about",  "know"]
        count = 0
        isGossip = False

        #determine if specific query
        isSpecific = False
        subject = None

        #LIST OF USERS
        users = []

        #get all possible facts 
        query = '''SELECT * FROM facts'''
        db = Database()
        results = db.query(query)
        db.close_conn()

        #generate a list of users mentioned in the db
        for result in results:
            users.append(result[0])
            knowers = result[2].split("; ")
            for knower in knowers:
                users.append(knower)

        #turn users into set
        users = set(users)
        contains_about = False

        #for each word in the message, determine if is keyword
        for (ndx, m) in enumerate(msg):
            if contains_about == True:
                isSpecific = True
                subject = m[0]                
                contains_about = False
            else:
                if m[0].lower() in keywords:
                    count+=1
                elif m[0].lower() in tell_me_gossip:
                    isGossip = True
                elif (State.users != None and  m[0] in State.users) or m[0] in users:
                    if m[0] == "about":
                        contains_about = True
                    else:
                        isSpecific = True
                        subject = m[0]                
                
            
        confidence = 0.0
        #confidence is high that it's gossip
        if isGossip:
            confidence = 1
        #if we know the query is targeted, we have high confidence
        elif isSpecific: 
            confidence = 1
        #we're a little less confident it's gossip
        else:
            confidence = count/len(keywords) 
            
        return (confidence, {'specific': isSpecific, 
                             'subject': subject, 
                             'isAffirmative' : True})


State.register(RespondGossip, True)
