"""
Pipelined processor that takes in a Filter, processes a message, and communicates with 
inference engine to retrieve correct response to user input.
"""

from nlp import filter
from filter import Filter

class MSGProcessor(object):
    def __init__(self, filter):
        self.filter = filter

    '''check the possible responses and choose one'''
    def respond(self, msg):
        filtMsg =  filter.filter(msg)

        #TODO (Kim) look up response in db
        #choose valid response
        response = callInference(filtMsg)
        return response

    '''to be subclassed'''
    def callInference(msg):
        pass

