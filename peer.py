import socket, hashlib, sys, os
import _thread as thread

from time import sleep

# Magicamente pega o IP do PC atual
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# Guarda o IP do Supernodo que esta conectado
superIp = '127.0.0.1'

# Lista que tera os files deste computador com seus Hashes
files = []

# PORTS and GROUPS
UCAST_PORT = 5003
JOIN_PORT = 4778

# COMMUNICATION
LET_ME_JOIN = 'LET ME JOIN'
NOTHING = 'NOTHING'
STILL_ALIVE = 'STILL ALIVE'
I_WANT = 'I WANT:'
TRADE_ME = 'TRADE ME:'

def peer(sIp):
	
    global superIp
	
    # Define o Supernodo
    superIp = sIp
	
    # Processou os files
    processFiles()
    
    ''' AQUI ELE OBRIGATORIAMENTE TEM QUE DAR JOIN ANTES DE PODER FAZER
    QUALQUER OUTRA COISA '''
	
    # Passo 1: Tenta dar join no SuperNodo escolhido
    JOIN_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    super_address = (superIp,JOIN_PORT)
    signal = bytes(LET_ME_JOIN,'utf-8')
    ''' SEND '''
    JOIN_sock.sendto(signal,super_address)
    ''' RECEIVE '''
    # Agora tenta escutar a resposta dele pra passar os dados
    rawdata, address = JOIN_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'ALLOWED':
        ''' SEND '''
        # ENVIA OS FILES
        for f in files:
            signal = bytes(f[0],'utf-8')
            JOIN_sock.sendto(signal,address)
            sleep(1)
            signal = bytes(f[1],'utf-8')
            JOIN_sock.sendto(signal,address)
            sleep(1)
        signal = bytes('DONE','utf-8')
        JOIN_sock.sendto(signal,address)
        
        
    ''' PEER ENTROU E ESTABELECEU CONEXAO COM O SUPERNODO.
    HORA AGORA DE SETTAR AS THREADS DELE, COM EXCECAO DO OVERLAY
    POR ENQUANTO '''
    
    thread.start_new_thread(userTrade,())
    thread.start_new_thread(listenMessage,())
    thread.start_new_thread(overlay,(JOIN_sock,))
     
    # DEBUGGING CRAP
    while True:
        print('Peer Running')
        sleep(3)
    
    
''' THREAD '''
def overlay(JOIN_sock):
    while True:
        signal = bytes(STILL_ALIVE,'utf-8')
        address = (superIp,JOIN_PORT)
        ''' SEND CONSTANTE '''
        JOIN_sock.sendto(signal,address)
        sleep(5)

    
''' THREAD '''
def userTrade():
    os.system('clear')
    print('AGORA DIGITE OU HASH QUE ESTA PROCURANDO')
    userFile = input()
    # I WANT:dutra ou I WANT:tr
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (superIp,UCAST_PORT)
    message = I_WANT+userFile
    signal = bytes(message,'utf-8')
    ''' SEND '''
    UNI_sock.sendto(signal,address)
    
    ''' RECEIVE '''
    rawdata,address = UNI_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    message_parts = data.strip(':')
    
    if message_parts[0] == 'NOTHING':
        print('\n Nao foi encontrado nada!!')
    if message_parts[0] == 'FOUND':
		
        foundFiles = []
        info = ''
        while info != 'DONE':
            peerFiles = []
            rawinfo,address = JOIN_sock.recvfrom(1024)
            ''' RECEIVE '''
            # AQUI EU VOU PEGAR DO SUPER NODO TODOS OS FILES
            # QUE FORAM TRANSPORTADOS PRA ELE.
            # O SUPER NODO TAMBEM VAI GARANTIR QUE O IP SEJA ENVIADO
            # O SUPERNODO DO MEIO NO CASO
            info = str(rawinfo).strip('b')[1:-1]
            if info != 'DONE':
                peerFiles.append(info)
                rawinfo,address = JOIN_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                peerFiles.append(info)
                rawinfo,address = JOIN_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                peerFiles.append(info)
                foundFiles.append(files)
		
        index = 0
        for f in foundFiles:
            print('\n\n\n\n\nEste file?')
            print(f)
            print('Digite 1 para sim e 0 para nao')
            choice = int(input())
            if choice == 1:
                address = (f[2],UCAST_PORT)
                message = TRADE_ME+f[0]
                signal = bytes(message,'utf-8')
                ''' SEND '''
                UNI_sock.sendto(signal,address)
                rawinfo,address = JOIN_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                text_file = open("tradefile.txt", "w")
                text_file.write(info)
                text_file.close()
                
    
    UNI_sock.close()
    

''' THREAD '''
# AQUI ELE VAI ESCUTAR TANTO MENSAGENS DE SUPERNODOS EXIGINDO
# QUE ELE AVALIE SE TEM ALGUM ARQUIVO OU MENSAGENS DE
# PEERS REQUISITANDO TROCA
def listenMessage():
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',UCAST_PORT))
    
    # TUDO ISSO ABAIXO DENTRO DE UM WHILE TRUE
    # AQUI A MENSAGEM TERA O DIFERENCIADOR, SEPARADO POR UM :
    # QUE SIMBOLIZA O ARQUIVO QUE ELE PEDIU OU O SEARCH DADO
    # LOGO PRECISAMOS DE UM STRIP PARA :
    while True:
        ''' RECEIVE '''
        rawdata,address = UNI_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        message_parts = data.strip(':')
    
        ''' RECEBE PEDIDO DO SUPERNODO PARA PROCURAR FILES '''
        if message_parts[0] == 'SEARCH':
            foundFiles = []
            search = message_parts[1]
            for f in files:
                if search in f[0] or search in f[1]:
                    foundFiles.append(f)
            # AGORA, TEM QUE MANDAR DE VOLTA PRO SUPERNODO OS
            # ARQUIVOS OU UM 'NOTHING'
            if len(foundFiles) == 0:
                signal = bytes(NOTHING,'utf-8')
                ''' SEND '''
                UNI_sock.sendto(signal,address)
            else:
                # ENVIA OS FILES
                for f in foundFiles:
                    signal = bytes(f,'utf-8')
                    UNI_sock.sendto(signal,address)
                    sleep(1)
                signal = bytes('DONE','utf-8')
                UNI_sock.sendto(signal,address)
            
            
        ''' RECEBE PEDIDO DE UM PEER PARA TROCAR FILE '''
        if message_parts[0] == 'TRADE ME':
            with open(message.parts[1], 'r') as f:
                data = f.read().replace('\n', '')
                signal = bytes(data,'utf-8')
                ''' SEND '''
                UNI_sock.sendto(signal,address)
        
        
''' DONE!!! '''
def processFiles():
	
    global files
	
    for f in os.listdir('cases'):
        hashName = hashlib.md5(f.encode('utf-8')).hexdigest()
        files.append([f,hashName])
