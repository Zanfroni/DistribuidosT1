import socket
import _thread as thread

from time import sleep

ip = 'localhost'
superIp = 'loopback'
fileName = 'file'

#groups and ports
SUPNODE_PORT = 5003

# texts to communicate
CONNECT_TO_SUPER = 'LET ME JOIN'
STILL_ALIVE = 'STILL ALIVE'

def peer(sIp,fileN,pIp):
    
    ip = pIp
    superIp = sIp
    fileName = fileN
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # aqui o user digita o port, pq tem que estar disponível
    #SUPNODE_PORT = int(input())
    thread.start_new_thread(joinSuperNode, (sock,))
    # Agora que ele mandou pro SUPERNODE, espera a resposta dele
    data, address = sock.recvfrom(1024).strip('b')[1:-1]
    print('JOINED SUPERNODE: ' + data)
    if data = 'ALLOWED':
        # AQUI ELE CONFIRMA SE ELE JOINOU OU NAO. Se confirmou, cria Thread do IM ALIVE
        # Nota-se que se o supernodo arrancar ele fora da lista, a interface continua intacta
        # mas qlqr tentativa de conexao vai dar em merda
        
        ''' CRIAR THREAD QUE HASHEIA O FILE DO PEER '''
        ''' CRIAR THREAD QUE MANDA AS INFOS DA PORRA DO PEER PRO SUPERNODE '''
        
        thread.start_new_thread(stillAlive, (sock,))
        
        options()
        #Aqui agora ele tem que criar Thread que escuta um Supernodo pra estabelecer conexao com outro Peer
        
        #Aqui agora tem que criar o bagulho de pedir pra um supernodo um arquivo
    else: print('Not allowed to join')
    
def options():
    return

def joinSuperNode(sock):
    server_addr = (superIp,SUPNODE_PORT)
    signal = bytes(CONNECT_TO_SUPER, 'utf-8')
    sock.sendto(signal,server_addr)

def stillAlive(sock):
    #try except pra joinar outro??
    while True:
        server_addr = (superIp,SUPNODE_PORT)
        signal = bytes(STILL_ALIVE, 'utf-8')
        sock.sendto(signal,server_addr)
        sleep(5)
