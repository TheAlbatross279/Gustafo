from bot import *
from adapters.cliadapter import CLIAdapter
from db import SQLiteConn

beemo = Bot(CLIAdapter())

beemo.start()
