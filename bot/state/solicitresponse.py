from state import State
import random
from giveupstate import GiveUpState

class SolicitResponse(State):
    @staticmethod
    def respond(context):
        solicitations = ["Hello?",
                         "You should really put an away message up...",
                         "Are you there?",
                         "AYT?",
                         "Hey, " + context['_nick'] + ", you there?" ]

        rand_ndx = random.randint(0, len(solicitations) - 1)

        return solicitations[rand_ndx]

    @staticmethod
    def nextStates():
        return tuple([GiveUpState])

State.register(SolicitResponse)
