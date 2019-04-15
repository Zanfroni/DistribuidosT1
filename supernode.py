import socket, struct
import _thread as thread

from time import sleep

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
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    MCAST_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    thread.start_new_thread(peerJoin, ())
    while True:
        # Faz um receive dele. Essa porra pode tanto ser Uni como Multi
        print('running')
        sleep(2)
		
		

def peerJoin():
	# provavelmente while true pra se repetir com Peers
    UNI_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UNI_sock.bind(('',SUPNODE_PORT))
    print('quer ver')
    rawdata, address = UNI_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'LET ME JOIN':
        signal = bytes(ALLOWED_JOIN,'utf-8')
        UNI_sock.sendto(signal,address)
        
        rawdata, address = UNI_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        print('DUTRÃ ' + data)
        #peers.append(data)
        
        print('passei weee')
        thread.start_new_thread(stillAlive, (UNI_sock,))
        
    
def stillAlive(UNI_sock):
    count = 2
    while count > 0:
        rawdata, address = UNI_sock.recvfrom(1024)
        data = str(rawdata).strip('b')[1:-1]
        if data == 'STILL ALIVE':
            sleep(5)
            # Need to perfect this crap
    UNI_sock.close()
