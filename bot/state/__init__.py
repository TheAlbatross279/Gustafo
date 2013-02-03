"""
Gustafo is s knowledge based system that uses a state machine to transiition from one mode of chat to another. This package contains the states which Gustafo can enter.
"""

import os
import glob

for module in os.listdir(os.path.dirname(__file__)):
   if module == '__init__.py' or not module.endswith('.py'):
      continue
   __import__(module[:-3], locals(), globals())
del module
