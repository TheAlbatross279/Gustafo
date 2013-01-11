from state import State
import random
from solicituser import SolicitUser

class ILoveYouState(State):
    @staticmethod
    def recognize(msg):
        iloveyou =  ["i", "love", "you"]
        
        if len(msg) < len(iloveyou):
            return (0.0, {})

        for idx, w in enumerate(iloveyou):
            if msg[idx][0].lower() != w:
                   return (0.0, {})
                   
        return (1.0, {})

    @staticmethod
    def respond(context):
        State.forceState(SolicitUser,{'_nick': context['_nick']})

        solicitations = ["Do you want to hear some gossip?",
                         "Would you like me to tell you some gossip?",
                         "I know something really interesting. Would you like to hear about it?",
                         "I have some gossip, would you like me to share it with you?"]

        rand_ndx = random.randint(0, len(solicitations) - 1)

        return  "I love you too, " + context['_nick'] + "! " + solicitations[rand_ndx]

    @staticmethod
    def nextStates():
        return tuple([SolicitUser])

State.register(ILoveYouState, True)
