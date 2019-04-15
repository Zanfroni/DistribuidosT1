import socket, hashlib, sys
import _thread as thread

from time import sleep

ip = 'localhost'
superIp = 'loopback'
fileName = 'file'
hashName = 'hash'

#groups and ports
SUPNODE_PORT = 5003

# texts to communicate
CONNECT_TO_SUPER = 'LET ME JOIN'
STILL_ALIVE = 'STILL ALIVE'

def peer(sIp,fileN,pIp):
    
    global superIp,ip,fileName
    
    ip = pIp
    superIp = sIp
    fileName = fileN
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # aqui o user digita o port, pq tem que estar disponível
    #SUPNODE_PORT = int(input())
    print('fucking shit')
    thread.start_new_thread(joinSuperNode, (sock,))
    # Agora que ele mandou pro SUPERNODE, espera a resposta dele
    rawdata, address = sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'ALLOWED':
        print('JOINED SUPERNODE: ' + data)
        # AQUI ELE CONFIRMA SE ELE JOINOU OU NAO. Se confirmou, cria Thread do IM ALIVE
        # Nota-se que se o supernodo arrancar ele fora da lista, a interface continua intacta
        # mas qlqr tentativa de conexao vai dar em merda
        
        ''' CRIAR THREAD QUE HASHEIA O FILE DO PEER '''
        thread.start_new_thread(setHash,())
        sleep(1)
        ''' CRIAR THREAD QUE MANDA AS INFOS DA PORRA DO PEER PRO SUPERNODE '''
        thread.start_new_thread(sendInfoSuper, ())
        
        thread.start_new_thread(stillAlive, (sock,))
        
        options()
        sys.exit()
        #Aqui agora ele tem que criar Thread que escuta um Supernodo pra estabelecer conexao com outro Peer
        
        #Aqui agora tem que criar o bagulho de pedir pra um supernodo um arquivo
    else: print('Not allowed to join')
    
def options():
    return

def sendInfoSuper():
	
	global ip, fileName, hashName
	
	# aqui deve se dar send via socket para o super node

def setHash():
	hashName = hashlib.md5(fileName.encode('utf-8')).hexdigest()

def joinSuperNode(sock):
    global superIp
	
    print('wtf')
    server_addr = (superIp,SUPNODE_PORT)
    signal = bytes(CONNECT_TO_SUPER, 'utf-8')
    print('wtf ' + str(signal))
    print('wtf ' + str(server_addr))
    print('whatafãq ' + str((signal,server_addr)))
    sock.sendto(signal,server_addr)
    print('wtf')

def stillAlive(sock):	
    #try except pra joinar outro??
    while True:
        server_addr = (superIp,SUPNODE_PORT)
        signal = bytes(STILL_ALIVE, 'utf-8')
        print(signal)
        print(server_addr)
        sock.sendto(signal,server_addr)
        sleep(5)
