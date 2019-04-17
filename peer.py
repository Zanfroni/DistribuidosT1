# BIBLIOTECAS NATIVAS DO PYTHON
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

'''
INICIO -> PARAMETRO DE ENTRADA SERA O IP DO SUPERNODO A SE CONECTAR
'''
def peer(sIp):
	
    global superIp
	
    # Define o Supernodo
    superIp = sIp
	
    # Processou os files
    processFiles()
    
    # AQUI ELE OBRIGATORIAMENTE TEM QUE DAR JOIN ANTES DE PODER FAZER
    # QUALQUER OUTRA COISA
	
    # Passo 1: Tenta dar join no SuperNodo escolhido
    JOIN_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    super_address = (superIp,JOIN_PORT)
    signal = bytes(LET_ME_JOIN,'utf-8')
    JOIN_sock.sendto(signal,super_address)
    # Agora tenta escutar a resposta dele pra passar os dados
    rawdata, address = JOIN_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'ALLOWED':

        # ENVIA OS FILES PARA O SUPERNODO QUE SE CONECTOU
        for f in files:
            signal = bytes(f[0],'utf-8')
            JOIN_sock.sendto(signal,address)
            sleep(1)
            signal = bytes(f[1],'utf-8')
            JOIN_sock.sendto(signal,address)
            sleep(1)
        signal = bytes('DONE','utf-8')
        JOIN_sock.sendto(signal,address)
        
    # COM A CONEXAO ESTABELECIDA, AS THREADS SAO INICIALIZADAS
    
    thread.start_new_thread(overlay,(JOIN_sock,))
    thread.start_new_thread(userTrade,())
    thread.start_new_thread(listenMessage,())
     
    # A CADA 10 SEGUNDOS, IMPRIME UMA NOTIFICACAO QUE O SISTEMA
    # AINDA ESTA FUNCIONANDO
    while True:
        print('Peer Running')
        sleep(10)
    
    
'''
THREAD

FUNCAO QUE MANDA MENSAGEM QUE AINDA ESTA VIVO PARA A CAMADA
DE OVERY A CADA 5 SEGUNDOS
UM SEND CONSTANTE BASICAMENTE
'''
def overlay(JOIN_sock):
    while True:
        signal = bytes(STILL_ALIVE,'utf-8')
        address = (superIp,JOIN_PORT)
        JOIN_sock.sendto(signal,address)
        sleep(5)

    
''' 
THREAD

ESTA FUNCAO IMPLEMENTA A INTERFACE QUE O USUARIO DIGITA
UM INPUT, QUE SERA UMA STRING DO ARQUIVO (OU SUBSTRING DELE
OU DO HASH) E TODO O PROCESSO DE BUSCA SERA INICIALIZADO
ESTA FUNCAO:
- MANDA PARA O SUPERNODO O QUE ELA ESTA PROCURANDO
- RECEBE LISTA E USUARIO DEVE ESCOLHER SE O RECURSO
QUE O MESMO ESTA PROCURANDO ESTA PRESENTE NA LISTA (ELE PODE
ACABAR RECEBENDO NADA TAMBEM, QUE ENCERRA O PROGRAMA)
-- SE NAO ESTIVER PRESENTE, SE ENCERRA O PROGRAMA
-- SE ESTIVER, SE COMUNICA COM O PEER QUE POSSUI E REALIZA
A TRANSFERENCIA

'''
def userTrade():
    os.system('clear')
    print('AGORA DIGITE OU HASH QUE ESTA PROCURANDO')
    userFile = input()
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (superIp,UCAST_PORT)
    message = I_WANT+userFile
    signal = bytes(message,'utf-8')
    UNI_sock.sendto(signal,address)
    
    rawdata,address = UNI_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    message_parts = data.split(':')
    if message_parts[0] == 'NOTHING':
        print('NAO EXISTE NADA DO QUE PROCURASTE NA REDE!!')
        print('TENTE NOVAMENTE!!')
        sleep(2)
        os.system('clear')
    if message_parts[0] == 'FOUND':
        potential = []
        info = ''
        while info != 'DONE':
            listFiles = []
            rawinfo,address = UNI_sock.recvfrom(1024)
            info = str(rawinfo).strip('b')[1:-1]
            if info != 'DONE':
                listFiles.append(info)
                rawinfo,address = UNI_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                listFiles.append(info)
                rawinfo,address = UNI_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                listFiles.append(info)
                potential.append(listFiles)
		
        index = 0
        for f in potential:
            print('\n\n\n\n\nEste file?')
            print(f)
            print('Digite 1 para sim e 0 para nao')
            choice = int(input())
            if choice == 1:	
                address = (f[2],UCAST_PORT)
                message = TRADE_ME+f[0]
                signal = bytes(message,'utf-8')
                UNI_sock.sendto(signal,address)
                rawinfo,address = UNI_sock.recvfrom(1024)
                info = str(rawinfo).strip('b')[1:-1]
                text_file = open("tradefile.txt", "w")
                text_file.write(info)
                text_file.close()
                print('tradefile.txt gerado. Transferência feita com sucesso')
    
    UNI_sock.close()
    sleep(2)
    os.system('clear')
    repeatProcess()
    
# Apenas repete o processo, para que nao tenha que se criar outra
# Thread novamente
def repeatProcess():
    userTrade()
    


'''
THREAD

ESTA FUNCAO ESCUTA MENSAGENS:

- FETCH ME --> SUPERNODO PEDE PARA ELE PROCURAR UM RECURSO COM A
STRING DE ENTRADA PROPOSTA. ELE RETORNA UMA LISTA COMO TODOS QUE
POSSUEM (OU NADA)
- TRADE ME --> PEER MANDA MENSAGEM PARA ESTE REQUISITANDO TRANSFERENCIA
ESTE PEER MANDA O ARQUIVO QUE O OUTRO PEDE PARA O OUTRO

'''

def listenMessage():
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',UCAST_PORT))
    
    while True:
        rawdata,address = UNI_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        message_parts = data.split(':')
        if message_parts[0] == 'FETCH ME':

            for f in files:
                if (message_parts[1] in f[0]) or (message_parts[1] in f[1]):
                    signal = bytes(f[0],'utf-8')
                    UNI_sock.sendto(signal,address)
                    sleep(1)
                    signal = bytes(f[1],'utf-8')
                    UNI_sock.sendto(signal,address)
                    sleep(1)
            signal = bytes('DONE','utf-8')
            UNI_sock.sendto(signal,address)

        if message_parts[0] == 'TRADE ME':
            ''' PEGA O FILE, LE ELE E ENVIA TODO O CONTEXTO '''
            with open('cases/'+message_parts[1], 'r') as fileToTransfer:
                data = fileToTransfer.read().replace('\n', '')
                signal = bytes(data,'utf-8')
                UNI_sock.sendto(signal,address)    
    
     
'''
*** PROCESSA OS ARQUIVOS:
- ENTRA NO DIRETORIO cases/
- PEGA CADA NOME DE ARQUIVO E CRIA O HASH
- INSERE NA LISTA files --> (file,hash)
- ELE NAO GUARDA EM files O SEU IP
'''
def processFiles():
	
    global files
	
    for f in os.listdir('cases'):
        hashName = hashlib.md5(f.encode('utf-8')).hexdigest()
        files.append([f,hashName])
