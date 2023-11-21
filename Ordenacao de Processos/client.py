import socket
import config
from time import sleep
from copy import deepcopy

def run_client():
    # (tempo de realização do evento, destino) 
    

    '''
    events_queue = []
    
    # Figure 11.6 example - Coulouris, 4ed.
    if config.pid == 1:
        events_queue = [(1, ""), (4, config.ip_list[1])]
    elif config.pid == 2:
        events_queue = [(6, config.ip_list[2])]
    else:
        events_queue = [(2, "")]
    '''

    for event in config.events_queue:
        # Esperar o tempo de realização do evento
        print(f"Waiting {event[0]} second(s)...")
        sleep(event[0])
        # Travar para acessar seção crítica
        config.lock.acquire()
        config.event_count += 1
        # Destravar seção
        config.lock.release() 
        
        # se o endereço de destino não for vazio
        if(event[1] != ''):
            # envia uma requisição
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Incrementar contador - registrar novo evento
                print(f"Sending a message to {event[1]}")
                s.connect((event[1], config.port))
                s.sendall(str(config.event_count).encode())
        # adiciona o evento na lista de ventos
        # Travar para acessar seção crítica
        config.lock.acquire()
        # Adiciona na lista o relógio lógico e o id do processo
        # O id do evento pode ser criado como "relogio_logico.pid"
        # Por exemplo, o evento 2.1 é o segundo evento que ocorreu no processo 1
        print(f"Adicionando evento LOCAL: ({config.event_count}, {config.pid})")
        config.event_list.append((config.event_count, config.pid))
        # Destravar seção
        config.lock.release()        


    # Esperar para que todos os eventos ocorram
    sleep(10)

    # Adiciona lista de ventos locais para a lista de eventos globais, para sincronização
    config.event_list_global += config.event_list

    # Iniciar sincronização entre processos
    # percorre a lista de IPs enviando sua lista de ventos, exceto quando o IP corresponde a si mesmo
    for i in range(len(config.ip_list)):
        if i+1 != config.pid:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"Sending local event list to {config.ip_list[i]}")
                s.connect((config.ip_list[i], config.port))
                s.sendall(str(config.event_list).encode())