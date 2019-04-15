import socket, struct
import _thread as thread

from time import sleep

# IP and List of peer data
ip = 'localhost'
peers = []

# PORTS and GROUPS
MCAST_GRP = '224.3.29.71'
MCAST_PORT = 6969
UCAST_PORT = 5003
JOIN_PORT = 4778

# COMMUNICATION
ALLOWED_JOIN = 'ALLOWED'

def supernode(superIp):
	
    global ip, peers
    ip = superIp
    
    # Passo 1: Entrar no grupo de Multicast
    MCAST_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MCAST_sock.bind(('',MCAST_PORT))
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    MCAST_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    # Passo 2: Criar Thread para escuta
    thread.start_new_thread(listenMC, (MCAST_sock,))
    thread.start_new_thread(listenUNI, ())
    thread.start_new_thread(listenJoin, ())
    
    # DEBUG
    while True:
        print('running')
        sleep(2)
    
def listenMC(MCAST_sock):
	
    return
    #MCAST_sock = recvfrom(1024)

def listenUNI():
	
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',UCAST_PORT))
    rawdata,address = UNI_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    #if MESSAGE
    
def listenJoin():
	
    JOIN_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    JOIN_sock.bind(('',JOIN_PORT))
    rawdata,address = JOIN_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'LET ME JOIN':
        signal = bytes(ALLOWED_JOIN,'utf-8')
        JOIN_sock.sendto(signal,address)
        
        sleep(2)
        rawinfo,address = JOIN_sock.recvfrom(1024)
        info = str(rawinfo).strip('b')[1:-1]
        peers.append(info)
        print(peers)
    
