import socket, struct
import _thread as thread
import time

from time import sleep

# Magicamente pega o IP do PC atual
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

''' AQUI PRA CIMA ESTA TUDO OK '''

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

def supernode():
	
    global peers
    
    # Assim que criado, ele gera 3 Threads:
    # Uma para escutar na PORTA Multicast
    # Uma para escutar na PORTA Unicast
    # Uma para escutar em outra PORTA Unicast Peers que querem entrar (necessario por causa do Overlay)
    thread.start_new_thread(listenMC, ())
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
        ''' RECEIVE '''
        rawdata, address = MCAST_sock.recvfrom(1024)
        MCAST_RESPONSE = address
        print('RECEBI MULTICAST DUTRA')
        data = str(rawdata).strip('b')[1:-1]
        message_parts = data.split(':')
        print('MSGN DUTRA ' + str(message_parts))
        print()
    
        #print ('received %s bytes from %s' % (len(data), address))
        #print (data)

        '''and address[0] != ip'''
        if message_parts[0] == 'DO YOU HAVE' and address[0] != ip:
            print('FEITOOOOOOOOO')
            
            ''' AGORA O FILHO DA PUTA DO DUTRA TEM QUE MANDAR A MSGN PRA TODOS OS
            NODINHOS QUE ESTÃO CONECTADOS A ELE. PRECISO DE EXTRAÇÃO DOS PEERS '''
            
            nodes = []
            print(peers)
            for p in peers:
                if p[2] not in nodes:
                    nodes.append(p[2])
            
            # NODES É SÓ OS IPS DOS QUE TAO CONECTADOS A ELE
            # OS QUAIS ELE TEM QUE MANDAR UNI UNI
            print(nodes)
            
            # FOI, AGORA, TEM QUE MANDAR UNICAST PRA CADA UM DESSES IMBECIS E GARANTIR LISTA
            # COM O IP DELES, ASSIM COMO O QUE ELES RETORNAREM!!
            
            potentialFiles = []
            for p in nodes:
                ''' SEND '''
                TRADE_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                message = FETCH_ME+message_parts[1]
                signal = bytes(message,'utf-8')
                node = (p,UCAST_PORT)
                ''' SEND '''
                print()
                print('ENVIEI O LERINA')
                TRADE_sock.sendto(signal,node)
                print('FOI MEMO')
                # AGORA DE CADA DUTRA QUE ELE MANDA, TEM QUE RECEBER A PORRA DA RESPOSTA
                # SE TER ALGUMA RESPOSTA, QUE N SEJA NOTHING, ELE VAI GUARDAR
                
                # AGORA O RECEIVE VAI PEGAR ESSAS PORRA DE FILES
                # QUE É O POTENTIALFILES
                # PRA CADA P QUE EU MANDEI, VOU PEGAR AS DE CADA
                # E BOTAR NO POTENTIAL_FILES, ANEXANDO SEMPRE
                # O IP
                
                info = ''
                while info != 'DONE':
                    ''' RECEIVE CONTINUO '''
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
                print('POTENTIAL DUTRAS ' + str(potentialFiles))
                # AQUI DEVO BOTAR, SE POTENTIALFILES = [], NAO RESPONDER!!
                # E FECHAR O CICLO AQUI MESMO
                
            # SE O POTENTIAL FILES NAO ESTIVER VAZIO, TEM QUE TRANSMITIR
            # PARA O SUPERNODO QUE MANDOU O MC ANTES DO TIMEOUT
            
            ''' SEND FILHO DA PUTA '''
            # MANDANDO A MANADA PRO MULTICAST SUPERNODE
            if len(potentialFiles) != 0:
                for fileInfo in potentialFiles:
                    for f in fileInfo:
                        print('fail info ' + str(fileInfo))
                        print('fail info2222 ' + str(f))
                        signal = bytes(f,'utf-8')
                        TRADE_sock.sendto(signal,MCAST_RESPONSE)
                        sleep(1)
                signal = bytes('DONE','utf-8')
                print('cheguei aqui por acaso? ' + str(signal))
                TRADE_sock.sendto(signal,MCAST_RESPONSE)
                
            print('FECHEI O SOCKET')
            TRADE_sock.close()
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            


''' THREAD '''
def listenUNI():
	
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',UCAST_PORT))
    
    #TUDO ISSO ABAIXO DENTRO DE UM WHILE TRUE
    while True:
        ''' RECEIVE '''
        rawdata,address = UNI_sock.recvfrom(1024)
        if address != ip:
            data = str(rawdata).strip('b')[1:-1]
            message_parts = data.split(':')
            print('QUERO RECEBER UM DUTRÃ ' + str(message_parts))
            # AQUI TEREI [I WANT] e [dutra]
            print('message[0] ' + str(message_parts[0]))
            if message_parts[0] == 'I WANT':
            
                MSEND_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ttl = struct.pack('b', 1)
                MSEND_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                multicast_group = (MCAST_GRP,MCAST_PORT)
                message = DO_YOU_HAVE+message_parts[1]
                signal = bytes(message,'utf-8')
                print('CHEGUEI NO MULTIBOSTA? BELEZA!!!')
                print('QUE QUE EU TENHO AQUI ' + message)
                ''' SEND TO MULTICAST GROUP '''
            
                # SETTAR TIMEOUT DE 3 SEGUNDOS PRA N FICAR ESPERANDO PRA SEMPRE
                # Settar candidatos e o Nodo filho a responder de volta (guard info)
                MSEND_sock.settimeout(10)
                candidates = []
                nodeToRespond = address
            
                try:
                    sent = MSEND_sock.sendto(signal, multicast_group)
                
                    while True:
                        try:
                            while data != 'DONE':
                                ''' RECEIVE DOS CARAS MULTICAST VIA UNICAST '''
                                print('RECEBI UNI_DUTRAS DOS MULTI_DUTRAS!!!!!!!!!!!!!!!!!!')
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
                                    print('FIM DO LOOP DUTRA')
                        
                        except socket.timeout:
                            print ('TIME OUT DO SOCKET DO MCAST')
                            break
                        else:
                            print('Fechando socket com ' + str(candidates))
                            MSEND_sock.close()
                            break
                finally:
                    print ('closing socket')
                    MSEND_sock.close()
            
                # AGORA TENHO QUE ENVIAR TODOS ESSES CANDIDATOS PRO DUTRA UNI
                # FILHO DA PUTA QUE ME PEDIU EM PRIMEIRO LUGAR
            
                response = nodeToRespond
                if len(candidates) == 0:
                    signal = bytes(NOTHING,'utf-8')
                    UNI_sock.sendto(signal,response)
                else:
                    # AGORA, MANDAR TUDO PRA ELE DE NOVO COM DONE (affs)
                    ''' SENDÃO MAROTAO '''
                
                    signal = bytes(FOUND,'utf-8')
                    UNI_sock.sendto(signal,response)
                    sleep(1)
                
                    ''' SEND FILHO DA PUTA '''
                    # MANDANDO A MANADA PRO MULTICAST SUPERNODE
                    for fileInfo in candidates:
                        for f in fileInfo:
                            print('fail info ' + str(fileInfo))
                            print('fail info2222 ' + str(f))
                            signal = bytes(f,'utf-8')
                            UNI_sock.sendto(signal,response)
                            sleep(1)
                    signal = bytes('DONE','utf-8')
                    print('MANDEI DE VOLTA PRO DUTRINHA JUNIOR ALFIO MARTINI ' + str(signal))
                    UNI_sock.sendto(signal,response)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        '''        
        # DEPOIS QUE TODA ESSA JOCA FUDIDA TER SIDO FEITA
        # HORA DE MANDAR PRO NODO SIM OU NAOdef stopwatch(seconds):
    start = time.time()
    # time.time() returns the number of seconds since the unix epoch.
    # To find the time since the start of the function, we get the start
    # value, then subtract the start from all following values.
    time.clock() 
        
            if len(candidates) > 0:
                signal = bytes(NOTHING,'utf-8')
                SEND
                UNI_sock.sendto(signal,leafAddr)
            
            # CONTINUAR DAQUI, QUANDO ELE TEM ARQUIVOS PARA MANDAR    
            else:
                return
        
        
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
	
    while True:
    
        JOIN_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        JOIN_sock.bind(('',JOIN_PORT))
        ''' RECEIVE '''
        # RECEBE O LET ME JOIN
        print('THREAD LISTENJOIN ESTA OUVINDO!')
        rawdata,address = JOIN_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        if data == 'LET ME JOIN':
            signal = bytes(ALLOWED,'utf-8')
            ''' SEND '''
            # MANDA O ALLOWED PARA O NODO JOINAR
            print('THREAD LISTENJOIN ESTA MANDANDO!')
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
            if len(peers) == 1:
                thread.start_new_thread(overlay,())
            
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
