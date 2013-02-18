"""
Pipelined processor that takes in a Filter, processes a message, and communicates with 
inference engine to retrieve correct response to user input.
@author Kim Paterson
"""

from processor.nlp.filter.filter import Filter

class MSGProcessor(object):
    def __init__(self, filter):
        self.filter = filter

    '''check the possible responses and choose one'''
    def respond(self, msg):
        filtMsg =  self.filter.filter(msg)


        #choose valid response
        response = self.call_inference(filtMsg)
        return response

    '''to be subclassed'''
    def call_inference(self, msg):
        pass

