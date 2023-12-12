import socket
import config
import threading
from time import sleep

def timeout(addr):
    target  = config.timeout * 100
    for i in range(0,target):
        if nodes_thread[addr][1].is_set():
            nodes_state[addr] = 0
            print(f"Processo de {addr} definido como NÃO suspeito!")
            nodes_thread[addr][1].clear()
            return
        sleep(0.01)
    print(f"Processo de {addr} definido como suspeito")
    nodes_state[addr] = 1

# Hashmap para o detector de falhas não confiável (Coulouris, 2007, p. 409)
# Para cada IP, é associado um número respectivamente representando:
# 0 --> Não suspeito
# 1 --> Suspeito
nodes_state = dict()
for i in range(len(config.ip_list)):
    nodes_state[config.ip_list[i]] = 1


nodes_thread = dict()
for i in range(len(config.ip_list)):
    nodes_thread[config.ip_list[i]] = [None, threading.Event()]


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # IP da pŕopria maquina
        print(f"Iniciando em: {config.ip_list[config.pid-1]}, {config.port}")
        s.bind((config.ip_list[config.pid-1], config.port))
        while True:
            s.listen()
            conn, addr = s.accept()
            addr = addr[0]
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    else:
                        received_data = data.decode('utf-8')    
                        # se ja existe uma thread rodando:
                        if(nodes_thread[addr][0] is not None and nodes_thread[addr][0].is_alive()):
                            print(f"Resetando evento do processo {addr}")
                            # mata a thread que estava rodando
                            nodes_thread[addr][1].set()
                            # abre uma trehad que vai marcar como suspeito caso estoure o tempo
                            nodes_thread[addr][0].join()
                        # inicia nova thread de timeout
                        print(f"(Re)iniciando função de timeout do processo {addr}")
                        nodes_thread[addr][0] = threading.Thread(target=timeout, args=[addr])
                        nodes_thread[addr][0].start()

if __name__ == "__main__":
    run_server()