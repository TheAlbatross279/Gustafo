from state import State
import random
from userresponse import UserResponse

class SolicitUser(State):
    @staticmethod
    def respond(context):
        solicitations = ["Do you want to hear some gossip?",
                         "Would you like me to tell you some gossip?",
                         "I know something really interesting. Would you like to hear about it?",
                         "I have some gossip, would you like me to share it with you?"]

        rand_ndx = random.randint(0, len(solicitations) - 1)

        return solicitations[rand_ndx]

    @staticmethod
    def nextStates():
        return tuple([UserResponse])

State.register(SolicitUser)
