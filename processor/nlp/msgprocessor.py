"""
Pipelined processor that takes in a Filter, processes a message, and communicates with 
inference engine to retrieve correct response to user input.
"""

from processor.nlp.filter import filter

class MSGProcessor(object):
    def __init__(self, filter):
        self.filter = filter

    '''check the possible responses and choose one'''
    def respond(self, msg):
        filtMsg =  filter.Filter(msg)

        #choose valid response
        response = call_inference(filtMsg)
        return response

    '''to be subclassed'''
    def call_inference(msg):
        pass

