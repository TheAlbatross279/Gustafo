from state import State

class Help(State):
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
        
