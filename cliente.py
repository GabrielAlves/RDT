import threading
import socket
import pickle

from pacote import Pacote
from segmento import Segmento

class Cliente:
    def __init__(self):
        self.nome_do_computador = socket.gethostname()
        self.ip_de_origem = socket.gethostbyname(self.nome_do_computador)
        self.ip_de_destino = "127.0.0.1"  # Trocar pelo ip do computador C
        self.porta_de_destino = 65432
        self.porta_de_origem = -1
        self.comprimento_do_buffer = 10000

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

        try:
            self.cliente.connect(("127.0.0.1", self.porta_de_destino))        

        except:
            return print('\nNão foi possívvel se conectar ao servidor!\n')

        # self.usuario = input('Usuário> ')
        print('\nConectado')

        self.receber_porta_de_origem_do_servidor()

        thread1 = threading.Thread(target=self.receber_mensagens)
        thread2 = threading.Thread(target=self.enviar_mensagens)
        thread1.start()
        thread2.start()

    def enviar_mensagens(self):
        while True:
            try:
                mensagem = input('\n')
                comprimento = mensagem.encode("utf-8")

                segmento = Segmento(self.porta_de_origem, self.porta_de_destino, mensagem)
                pacote = Pacote(self.ip_de_origem, self.ip_de_destino, segmento)
                pacote_serializado = pickle.dumps(pacote)
                self.cliente.send(pacote_serializado)
                
            except:
                return

    def receber_mensagens(self):
        while True:
            try:
                pacote_serializado = self.cliente.recv(self.comprimento_do_buffer)  
                pacote = pickle.loads(pacote_serializado)
                segmento = pacote.retornar_segmento()
                mensagem = segmento.retornar_mensagem()
                print(f"mensagem enviada por {pacote.retornar_ip_de_origem()}: {mensagem}\n")

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.cliente.close()
                break

    def receber_porta_de_origem_do_servidor(self):
        while True:
            try:
                self.porta_de_origem = int(self.cliente.recv(self.comprimento_do_buffer).decode())
                print(type(self.porta_de_origem))
                print(self.porta_de_origem)
                break

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.cliente.close()
                break

if __name__ == "__main__":
    Cliente()