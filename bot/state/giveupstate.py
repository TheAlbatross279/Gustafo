from state import State
import random

class GiveUpState(State):
    @staticmethod
    def respond(context):
        frustrated_responses = ["Well, fine. Be that way", 
                                "Well... I'll catch you later then!",
                                "G2G! TTYL!"]

        rand_ndx = random.randint(0, len(frustrated_responses) - 1)
        
        return frustrated_responses[rand_ndx]

State.register(GiveUpState)
