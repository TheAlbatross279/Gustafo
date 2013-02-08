"""
Handles communication between DB and ChitChat State by processing 
messages and communicating with the db to find response.
"""

from processor.nlp.msgprocessor import MSGProcessor
from processor.inference import CCInferenceEngine

class ChitChatProcessor(MSGProcessor):
   def __init__(self, filter):
      super.__init__(filter)
      self.CCIE = CCInferenceEngine()
      
   def call_inference(msg):
      return self.CCIE.infer(msg)
      
