# Lista de ip dos nós da rede
#ip_list = ['191.52.7.28', '191.52.7.27', '191.52.7.26']
ip_list = [f"191.52.7.{i}" for i in range(28,10,-1)]

# Porta usada para a comunicação
port = 5000

# pid do nó local
# Deve ser alterado para corresponder o índice da lista de ip
# referente ao endereço da máquna local
pid = 1

# Tempo (em segundos) que o cliente espera para submeter
# uma mensagem de ping - identificado seu estado como não suspeito
sleep_time = 10

# Tempo (em segundos) que o servidor aguarda para então classificar
# um processo como suspeito
timeout = sleep_time + 2