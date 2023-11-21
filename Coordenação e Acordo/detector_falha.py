from config import *
from time import sleep
from client import *
from server import *
import  threading
import sys

config.pid = int(sys.argv[1])

client_thread = threading.Thread(target=run_client)
server_thread = threading.Thread(target=run_server)

client_thread.start()
server_thread.start()

client_thread.join()
server_thread.join()