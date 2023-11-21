import threading

port = 5000
pid = 1

ip_list = ['191.52.7.28', '191.52.7.27', '191.52.7.26']

lock = threading.Lock()

# (nome do evento, contador relógio lógico, pid)
event_list = []           
event_list_global = []         
event_count = 0
events_queue = []