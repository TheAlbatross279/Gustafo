"""
Handles communication between DB and HelpChat State by processing 
messages and communicating with the db to find response.
"""

from processor.nlp.msgprocessor import MSGProcessor
from processor.inference.hInferenceEngine import HInferenceEngine

class HelpChatProcessor(MSGProcessor):
   def __init__(self, filter):
      super(HelpChatProcessor, self).__init__(filter)
      self.HIE = HInferenceEngine()
      
   def call_inference(self, msg):
      return self.HIE.infer(msg)
      
