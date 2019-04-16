import socket, struct
import _thread as thread

from time import sleep

# Magicamente pega o IP do PC atual
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

''' AQUI PRA CIMA ESTA TUDO OK '''

# Lista de Peers conectados a este Supernodo com seus files
peers = []

# PORTS and GROUPS
MCAST_GRP = '224.3.29.71'
MCAST_PORT = 6969
UCAST_PORT = 5003
JOIN_PORT = 4778

# COMMUNICATION
ALLOWED = 'ALLOWED'
DO_YOU_HAVE = 'DO YOU HAVE:'
I_HAVE = 'I HAVE:'
NOTHING = 'NOTHING'

def supernode():
	
    global peers
    
    # Assim que criado, ele gera 3 Threads:
    # Uma para escutar na PORTA Multicast
    # Uma para escutar na PORTA Unicast
    # Uma para escutar em outra PORTA Unicast Peers que querem entrar (necessario por causa do Overlay)
    '''thread.start_new_thread(listenMC, ())'''
    thread.start_new_thread(listenUNI, ())
    thread.start_new_thread(listenJoin, ())
    
    # DEBUG
    while True:
        print('Supernode Running')
        sleep(3)

def listenMC():
	
	# Passo 1: Entrar no grupo de Multicast
    MCAST_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MCAST_sock.bind(('',MCAST_PORT))
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    MCAST_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	
    while True:
        #print ('\nwaiting to receive message')
        rawdata, address = sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        message_parts = data.strip(':')
    
        #print ('received %s bytes from %s' % (len(data), address))
        #print (data)

        if message_parts[0] == 'FETCH ME' and address[0] != ip:
            #print ('sending acknowledgement to', address)
            ''' AQUI SERIA A LOGICA DE PROCURA '''
            fileList = searchForFile()
            ''' AGORA, ELE TEM QUE MANDAR DE VOLTA SE TEM '''
            ''' IF LIST NOT VAZIA, MANDAR ESSA LIST TODA '''
            #signal = bytes('HAVE_FILE'+fileList,'utf-8')
            #sock.sendto(signal, address)


''' THREAD '''
def listenUNI():
	
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',UCAST_PORT))
    
    #TUDO ISSO ABAIXO DENTRO DE UM WHILE TRUE
    while True:
        ''' RECEIVE '''
        rawdata,address = UNI_sock.recvfrom(1024)
        leafAddr = address
        data = str(rawdata).strip('b')[1:-1]
        message_parts = data.strip(':')
        # AQUI TEREI [I WANT] e [dutra]
        if message_parts[0] == 'I WANT':
            
            MSEND_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ttl = struct.pack('b', 1)
            MSEND_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            multicast_group = (MCAST_GRP,MCAST_PORT)
            message = DO_YOU_HAVE+message_parts[1]
            signal = bytes(message,multicast_group)
            ''' SEND TO MULTICAST GROUP '''
            
            # SETTAR TIMEOUT DE 3 SEGUNDOS PRA N FICAR ESPERANDO PRA SEMPRE
            MSEND_sock.settimeout(3)
            candidates = []
            
            try:
                sent = MSEND_sock.sendto(signal, multicast_group)
                
                while True:
                    try:
                        ''' RECEIVE DOS CARAS MULTICAST VIA UNICAST '''
                        rawdata, server = MSEND_sock.recvfrom(1024)
                        data = str(rawdata).strip('b')[1:-1]
                        message_parts = data.strip(':')
                    except socket.timeout:
                        print ('TIME OUT DO SOCKET DO MCAST')
                        break
                    else:
                        if message_parts[0] == 'I HAVE':
                            #print ('received "%s" from %s' % (data, server))
                            candidates.append((message_parts[1],message_parts[2]))
            finally:
                print ('closing socket')
                MSEND_sock.close()
        
        
        # DEPOIS QUE TODA ESSA JOCA FUDIDA TER SIDO FEITA
        # HORA DE MANDAR PRO NODO SIM OU NAO
        
            if len(candidates) > 0:
                signal = bytes(NOTHING,'utf-8')
                ''' SEND '''
                UNI_sock.sendto(signal,leafAddr)
            
            # CONTINUAR DAQUI, QUANDO ELE TEM ARQUIVOS PARA MANDAR    
            else:
                return
            '''
        
        
            EU REALMENTE PRECISO REVISAR E COMEÇAR A JA IR EXECUTANDO O
            MEU CODIGO. PRECISO IMEDIATAMENTE CORRIGIR AS CAGADAS QUE
            VÃO ACONTECER (THEY'RE BOUND TO HAPPEN)
            BORA TERMINAR ESSA PARTE RAPIDAMENTE AMANHA DE MANHÃ!!!
            E COMEÇAR A APLICAR AS CORREÇÕES DEVIDAMENTE
        
            '''
        
        
''' AQUI PRA BAIXO ESTA TUDO OK DONT FUCKING DISTURB MY ASS '''        
        
''' THREAD AQUI'''
# Nesta PORTA, ele escuta por Peers que querem entrar e permite entrada
# dos mesmos, assim como registro de seus arquivos e hashes respectivos,
# guardando junto seu IP para cada um    
def listenJoin():
	
    JOIN_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    JOIN_sock.bind(('',JOIN_PORT))
    ''' RECEIVE '''
    # RECEBE O LET ME JOIN
    rawdata,address = JOIN_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'LET ME JOIN':
        signal = bytes(ALLOWED,'utf-8')
        ''' SEND '''
        # MANDA O ALLOWED PARA O NODO JOINAR
        JOIN_sock.sendto(signal,address)
        
        ''' RECEIVE '''
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
