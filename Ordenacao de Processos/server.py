# funcao que fica recebendo:
import socket
import config

def run_server():
    listas_recebidas = 0        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # IP da pŕopria maquina
        s.bind((config.ip_list[config.pid-1], config.port))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    else:
                        received_data = data.decode('utf-8')
                        
                        try:
                            #converte para inteiro, o valor do cont recebido
                            time_received = int(received_data)
                            print(f"Evento recebido no tempo : {time_received}")
                            # Seção Crítica - INICIO
                            config.lock.acquire()
                            print(f"Pegando valor maximo entre ({config.event_count}, {time_received}) e somando 1")
                            # o contador atual recebe o valor maximo entre si e o recebido
                            config.event_count = max(config.event_count, time_received)
                            # incrementa o contador por ser um novo evento
                            config.event_count = config.event_count + 1
                            # adiciona o evento a sua lista
                            print(f"Adicionando evento REMOTO: ({config.event_count}, {config.pid})")
                            config.event_list.append((config.event_count, config.pid))    
                            # Seção Crítica - FIM 
                            config.lock.release()
                        
                        # Se existir erro de conversão (linha 24), significa que o dado recebido é uma lista de eventos - usada para sincronização 
                        except:
                            # Converter dado recebido para lista de eventos de outro processo
                            received_list = eval(received_data)
                            # Concatenar lista local de eventos com a lista recebida
                            print("*** recebendo lista de processo:")
                            config.event_list_global += received_list
                            #adiciona ao contador de listas recebidas
                            listas_recebidas = listas_recebidas + 1
                            
            # se contador de listas recebidas chega a 2, para
            if(listas_recebidas >= 2):
                break
                    

