"""
Handles communication between DB and ChitChat State by processing 
messages and communicating with the db to find response.
"""

from processor.nlp.msgprocessor import MSGProcessor
from processor.inference.ccInferenceEngine import CCInferenceEngine

class ChitChatProcessor(MSGProcessor):
   def __init__(self, filter):
      super(ChitChatProcessor, self).__init__(filter)
      self.CCIE = CCInferenceEngine()
      
   def call_inference(self, msg):
      return self.CCIE.infer(msg)
      
