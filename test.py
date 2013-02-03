from bot import *
from adapters import CLIAdapter
from db import SQLiteConn

beemo = Bot(CLIAdapter())

beemo.start()
