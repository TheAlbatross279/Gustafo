from state import State
#from 

class ChitChat(State):
    def __init__(self):
        self.processor = MSGProcessor()

    @staticmethod
    def recognize(msg):
        return (1.0, {})
    
    @staticmethod
    def respond(context):
        response = processor(msg)
        return response

#State.register(ChitChat, True)
        
