# BIBLIOTECAS NATIVAS DO PYTHON
import os
from time import sleep

# CHAMADAS DE FUNCOES
from peer import peer
from supernode import supernode

'''
AQUI SERA O INICIO DO CODIGO
O USUARIO DEVE EXECUTAR ESTE MODULO PARA INICIAR
ELE DEVE DIGITAR supernode OU peer PARA DEFINIR
O QUE SEU COMPUTADOR VAI SER
SE FOR peer, ELE DEVE DIGITAR O IP DO supernode
QUE DESEJA SE CONECTAR

QUALQUER ERRO O SISTEMA ENTRA NO EXCEPT E IMPRIME UMA MENSAGEM
DE ERRO AO INVES DE UM EXCEPTION
'''
def main():
    try:
        while True:
            print('Digite o seu papel (peer ou supernode):')
            device = input()
            clear()
            if device == 'supernode':
                clear()
                supernode()
                break
            elif device == 'peer':
                print('\nDigite corretamente o IP do Supernodo a se contectar:')
                superIp = input()
                clear()
                peer(superIp)
                break
            else:
                # Se o usuario nao digitar nem supernode ou peer
                # Ele cai nessa condicao e pode tentar de novo em 2 segundos
                print('Entrada invalida. Tente novamente em dois segundos')
                sleep(2)
                clear()
    except:
        clear()
        print('Erro fatal. Reinicie o programa e tente novamente.')
        return
        
        
def clear():
    os.system('clear')

if __name__ == "__main__":
    main()
