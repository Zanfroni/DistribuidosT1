import socket, struct
import _thread as thread

ip = 'localhost'

#peers (file,hash,peer ip)
peers = []

# Groups and ports
MCAST_GRP = '224.3.29.71'
MCAST_PORT = 6969
SUPNODE_PORT = 5003

# texts to communicate
ALLOWED_JOIN = 'ALLOWED'

def supernode(superIp):
    
    ip = superIp
    
    MCAST_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MCAST_sock.bind(('',MCAST_PORT))
    group = MCAST_sock.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    MCAST_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    # now that ele esta baindado no Multicast lixo do caralho, hora de ver as opcoes
    thread.start_new_thread(peerJoin, (,))
    
    # now that he joined, send the fucking listening options

def peerJoin():
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',SUPNODE_PORT))
    data, address = UNI_sock.recvfrom(1024).strip('b')[1:-1]
    if data == 'LET ME JOIN':
        # aqui eu deveria adicionar as merdas do peer
        thread.start_new_thread(stillAlive, (UNI_sock,))
    
def stillAlive():
    count = 2
    while count > 0:
        data, address = UNI_sock.recvfrom(1024).strip('b')[1:-1]
        if data == 'STILL ALIVE':
            sleep(5)
            # Need to perfect this crap
