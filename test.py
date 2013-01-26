from bot import *
from adapters import CLIAdapter

beemo = Bot(CLIAdapter(), None)

beemo.start()
