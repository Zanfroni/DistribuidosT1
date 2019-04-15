import os
from time import sleep

from peer import peer
from supernode import supernode

def main():
    #try:
    while True:
        print('Digite o seu papel (peer ou supernode):')
        device = input()
        clear()
        if device == 'supernode':
            print('\nDigite corretamente o IP do seu computador:')
            superIp = input()
            clear()
            supernode(superIp)
            break
        elif device == 'peer':
            print('\nDigite corretamente o IP do Supernodo a se contectar:')
            superIp = input()
            print('\nDigite corretamente um arquivo que este Peer possui:')
            fileName = input()
            print('\nDigite corretamente o IP do seu computador:')
            peerIp = input()
            clear()
            peer(superIp,fileName,peerIp)
            break
        else:
            print('Entrada invalida. Tente novamente em dois segundos')
            sleep(2)
            clear()
    #except:
        #clear()
        #print('Erro fatal. Reinicie o programa e tente novamente.')
        #return
        
        
def clear():
    os.system('clear')

if __name__ == "__main__":
    main()
