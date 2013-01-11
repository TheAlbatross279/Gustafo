from state import State
from secondaryoutreach import SecondaryOutreach

class InitiateState(State):
    @staticmethod
    def respond(context):
        return "Hello, " + context['_nick'] + "."

    @staticmethod
    def nextStates():
        return tuple([SecondaryOutreach])

State.register(InitiateState)
