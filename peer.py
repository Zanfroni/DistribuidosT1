import socket, hashlib, sys
import _thread as thread

from time import sleep

# Data
ip = 'localhost'
superIp = 'loopback'
fileName = 'file'
hashName = 'hash'

# PORTS and GROUPS
JOIN_PORT = 4778

# COMMUNICATION
CONNECT_TO_SUPER = 'LET ME JOIN'

def peer(sIp,fileN,pIp):
    
    global superIp,ip,fileName
    ip = pIp
    superIp = sIp
    fileName = fileN
    
    # Passo 1: Tenta dar join no SuperNodo escolhido
    JOIN_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    super_address = (superIp,JOIN_PORT)
    signal = bytes(CONNECT_TO_SUPER,'utf-8')
    JOIN_sock.sendto(signal,super_address)
    
    # Agora tenta escutar a resposta dele pra passar os dados
    rawdata, address = JOIN_sock.recvfrom(1024)
    data = str(rawdata).strip('b')[1:-1]
    if data == 'ALLOWED':
        setHash()
        
        info = fileName + ',' + hashName + ',' + ip
        signal = bytes(info,'utf-8')
        JOIN_sock.sendto(signal,address)
        ###

def setHash():
	
    global hashName
	
    hashName = hashlib.md5(fileName.encode('utf-8')).hexdigest()
