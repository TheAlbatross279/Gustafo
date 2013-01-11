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

        query = '''SELECT * FROM facts'''
        db = Database()
        results = db.query(query)
        db.close_conn()

        for result in results:
            users.append(result[0])
            knowers = result[2].split("; ")
            for knower in knowers:
                users.append(knower)

        users = set(users)
        contains_about = False

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
        elif isSpecific:
            confidence = 1
        #we're a little less confident it's gossip
        else:
            confidence = count/len(keywords) + 0.4
            
        return (confidence, {'specific': isSpecific, 
                             'subject': subject, 
                             'isAffirmative' : True})


State.register(RespondGossip, True)
