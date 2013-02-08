"""
Handles communication between DB and HelpChat State by processing 
messages and communicating with the db to find response.
"""

from processor.nlp.msgprocessor import MSGProcessor
from processor.inference import HInferenceEngine

class HelpChatProcessor(MSGProcessor):
   def __init__(self, filter):
      super.__init__(filter)
      self.HIE = HInferenceEngine()
      
   def callInference(msg):
      return self.HIE.infer(msg)
      
