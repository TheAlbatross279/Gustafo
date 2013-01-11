#CSC 481: Knowledge Based System Chatbot aka Gustafo

Gustafo is a chatbot that helps answer programming questions in addition to having a great personality.


## Adding New States
Here is an example of a very simple greeting state:

```Python
from state import State

# All states must inherit from another state
class HelloState(State):

  # The recognize method takes in a POS tagged message and returns a confidence value that
  # the given message belongs in this state along with any information the respond method
  # would need to formulate a response.
  @staticmethod
  def recognize(self, msg):
    if msg[0][0] == 'Hello':
      return (1, {})
    else:
      return (0, {})

  # The respond method is called if the confidence value returned in the recognize method is
  # higher than any other valud stat. It takes in the context returned from the recognize method
  # and does any processing the state would like to do in response. If a string is returned, the
  # message is sent to the chat, if None is returned, nothing happens.
  @staticmethod
  def respond(self, context):
    # The nickname of the user who messaged the bot will always be available in the context
    # under the '_nick' key.
    return "Hello there, " + context['_nick'] + "!"

# Immediately after the state is defined it is registered
# with the bot. The register method takes in a boolean which determines whether this state can
# be used to initiate conversation with a user. This value defaults to False.
State.register(HelloState, True)
```
