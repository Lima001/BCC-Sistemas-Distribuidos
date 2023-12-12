import socket
import config
from time import sleep

def run_client():
    while True:
        # percorre a lista de IPs enviando uma mesagem informando que esta funcionando
        for i in range(len(config.ip_list)):
            if i+1 != config.pid:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print(f"Tentando enviar mensagem para {config.ip_list[i]}")
                    try:
                        s.connect((config.ip_list[i], config.port))
                        s.sendall(f"{config.pid} esta aqui!".encode())
                    except:
                        print(f"Erro ao tentar enviar mensagem para {config.ip_list[i]}")

        
        # Esperar tempo padrão para a próxima sincronização
        sleep(config.sleep_time)

if __name__ == "__main__":
    run_client()