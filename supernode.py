# BIBLIOTECAS NATIVAS DO PYTHON
import socket, struct
import _thread as thread
import time
from time import sleep

# Magicamente pega o IP do PC atual
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# Lista de Peers conectados a este Supernodo com seus files
# elapsed e count vao ser parametros para a camada de overlay
peers = []
elapsed = 0
count = 2

# PORTS and GROUPS
MCAST_GRP = '224.3.29.71'
MCAST_PORT = 6969
UCAST_PORT = 5003
JOIN_PORT = 4778

# COMMUNICATION
ALLOWED = 'ALLOWED'
DO_YOU_HAVE = 'DO YOU HAVE:'
FETCH_ME = 'FETCH ME:'
I_HAVE = 'I HAVE:'
NOTHING = 'NOTHING'
FOUND = 'FOUND'


# INICIO
def supernode():
	
    global peers
    
    # Assim que criado, ele gera 3 Threads:
    # Uma para escutar na PORTA Multicast
    # Uma para escutar na PORTA Unicast
    # Uma para escutar em outra PORTA Unicast, Peers que querem entrar (necessario por causa do Overlay)
    thread.start_new_thread(listenJoin, ())
    thread.start_new_thread(listenUNI, ())
    thread.start_new_thread(listenMC, ())

    
    # A CADA 10 SEGUNDOS, IMPRIME UMA NOTIFICACAO QUE O SISTEMA
    # AINDA ESTA FUNCIONANDO
    while True:
        print('Supernode Running')
        sleep(10)

'''
THREAD

ESTA FUNCAO ESCUTA NA PORTA MULTICAST.
- ENTRA NO GRUPO MULTICAST E FICA ESCUTANDO
- QUANDO RECEBER TRANSMISSAO, VAI ATRAS DOS PEERS E PERGUNTA
PRA ELES SE ELES TEM O INPUT PROPOSTO
- RECEBE RESPOSTA DELES E MANDA DE VOLTA PARA O SUPERNODE QUE MANDOU

'''
def listenMC():
	
	# Passo 1: Entrar no grupo de Multicast
    MCAST_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MCAST_sock.bind(('',MCAST_PORT))
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    MCAST_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    while True:
        rawdata, address = MCAST_sock.recvfrom(1024)
        MCAST_RESPONSE = address
        data = str(rawdata).strip('b')[1:-1]
        message_parts = data.split(':')
        
        if message_parts[0] == 'DO YOU HAVE' and address[0] != ip:

            # Essa lista serve para filtrar todos os IPs
            # de seus peers, extraídos da estrutura abstrata
            nodes = []

            for p in peers:
                if p[2] not in nodes:
                    nodes.append(p[2])
            
            # Estes serao os arquivos em candidatos que ele encontrou
            # que serao mandados para o supernode que mandou
            # o multicast
            potentialFiles = []
            for p in nodes:

                TRADE_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                message = FETCH_ME+message_parts[1]
                signal = bytes(message,'utf-8')
                node = (p,UCAST_PORT)

                TRADE_sock.sendto(signal,node)
                
                info = ''
                while info != 'DONE':

                    newFile = []
                    rawinfo,address = TRADE_sock.recvfrom(1024)
                    info = str(rawinfo).strip('b')[1:-1]
                    if info != 'DONE':
                        newFile.append(info)
                        rawinfo,address = TRADE_sock.recvfrom(1024)
                        info = str(rawinfo).strip('b')[1:-1]
                        newFile.append(info)
                        newFile.append(address[0])
                        potentialFiles.append(newFile)

            if len(potentialFiles) != 0:
                for fileInfo in potentialFiles:
                    for f in fileInfo:
                        signal = bytes(f,'utf-8')
                        TRADE_sock.sendto(signal,MCAST_RESPONSE)
                        sleep(1)
                signal = bytes('DONE','utf-8')
                TRADE_sock.sendto(signal,MCAST_RESPONSE)
                
            TRADE_sock.close()
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            


'''

THREAD 

NESTA FUNCAO, ELE ESCUTA SEUS PEERS:
- RECEBE REQUISICAO DE RECURSO DE PEER
- TRANSMITE UM MULTICAST PARA O GRUPO
- VAI RECEBENDO DOS OUTROS SUPERNODES O QUE
RESPEITAVA A STRING DE ENTRADA ATE O TIMEOUT ESGOTAR
- MANDA ESTAS LISTAS PARA O PEER QUE REQUISITOU

'''
def listenUNI():
	
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',UCAST_PORT))
    
    while True:

        rawdata,address = UNI_sock.recvfrom(1024)
        if address != ip:
            data = str(rawdata).strip('b')[1:-1]
            message_parts = data.split(':')
            if message_parts[0] == 'I WANT':
            
                MSEND_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ttl = struct.pack('b', 1)
                MSEND_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                multicast_group = (MCAST_GRP,MCAST_PORT)
                message = DO_YOU_HAVE+message_parts[1]
                signal = bytes(message,'utf-8')
                
                ''' SEND TO MULTICAST GROUP '''
            
                # O timeout pode ser alterado aqui.
                # Escolhemos 10 segundos por parecer mais justo
                MSEND_sock.settimeout(10)
                candidates = []
                nodeToRespond = address
            
                # Transmissao Multicast iniciada
                # Quando o timeout estourar, ele sai e fecha o socket
                # que transmitiu
                try:
                    sent = MSEND_sock.sendto(signal, multicast_group)
                
                    while True:
                        try:
                            while data != 'DONE':
                                interceptedFiles = []
                                rawdata, server = MSEND_sock.recvfrom(1024)
                                data = str(rawdata).strip('b')[1:-1]
                                if data != 'DONE':
                                    interceptedFiles.append(data)
                                    rawdata,address = MSEND_sock.recvfrom(1024)
                                    data = str(rawdata).strip('b')[1:-1]
                                    interceptedFiles.append(data)
                                    rawdata,address = MSEND_sock.recvfrom(1024)
                                    data = str(rawdata).strip('b')[1:-1]
                                    interceptedFiles.append(data)
                                    candidates.append(interceptedFiles)
                        
                        except socket.timeout:
                            print ('TIME OUT DO SOCKET DO MCAST')
                            break
                        else:
                            print ('closing socket')
                            MSEND_sock.close()
                            break
                finally:
                    print ('closing socket')
                    MSEND_sock.close()
            
                response = nodeToRespond
                if len(candidates) == 0:
                    signal = bytes(NOTHING,'utf-8')
                    UNI_sock.sendto(signal,response)
                else:
                
                    signal = bytes(FOUND,'utf-8')
                    UNI_sock.sendto(signal,response)
                    sleep(1)

                    for fileInfo in candidates:
                        for f in fileInfo:
                            signal = bytes(f,'utf-8')
                            UNI_sock.sendto(signal,response)
                            sleep(1)
                    signal = bytes('DONE','utf-8')
                    UNI_sock.sendto(signal,response)
           
'''

THREAD

Nesta PORTA, ele escuta por Peers que querem entrar e permite entrada
dos mesmos, assim como registro de seus arquivos e hashes respectivos,
guardando junto seu IP para cada um   

''' 
def listenJoin():
	
    while True:
    
        JOIN_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        JOIN_sock.bind(('',JOIN_PORT))

        # RECEBE O LET ME JOIN
        rawdata,address = JOIN_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        if data == 'LET ME JOIN':
            signal = bytes(ALLOWED,'utf-8')
            
            # MANDA O ALLOWED PARA O NODO JOINAR
            JOIN_sock.sendto(signal,address)
            
            # RECEBE A LISTA DE FILES DELE
            info = ''
            while info != 'DONE':
                files = []
                rawinfo,address = JOIN_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                if info != 'DONE':
                    files.append(info)
                    rawinfo,address = JOIN_sock.recvfrom(1024)
                    info = str(rawinfo).strip('b')[1:-1]
                    files.append(info)
                    files.append(address[0])
                    peers.append(files)
                
            
            print(peers)
            if len(peers) == 1:
                thread.start_new_thread(overlay,())
           
           
'''
OVERLAY

ESTA PARTE ESTA BEM DESCRITA NO RELATORIO:

-overlay GARANTE QUE ELE RECEBA RESPOSTAS PARA RESTAURAR O CONTADOR
-counting VAI TENTAR ZERAR O CONTADOR SEMPRE

''' 
def overlay():
	
    global elapsed, count
	
    OVERLAY_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    OVERLAY_sock.bind('',JOIN_PORT)
    count = 2
    clock = True
    clock = thread.start_new_thread(counting,())
    while clock:
        rawdata,address = OVERLAY_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        if data == 'STILL ALIVE':
            count = 2
    peers.clear()
    return
    
    
        
def counting():
	
    global elapsed, count
	
    while count > 0:
	
        start = time.time()
        time.clock()
        while(elapsed <= 5):
            elapsed = time.time() - start
            sleep(0.5)
        count -= 1
    return false
