from bot import *
from adapters import CLIAdapter
from db import SQLiteConn

beemo = Bot(CLIAdapter(), SQLiteConn('db/gossip.db'))

beemo.start()
