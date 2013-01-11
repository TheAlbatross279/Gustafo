from state import State, StateCollection
from states.wikistate import WikiState

bot = StateCollection([WikiState])

print bot.query("Chris", "Tell me about John Adams")
