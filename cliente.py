import threading
import socket
import pickle
import time

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
        self.num_sequencia = 0
        self.mensagem = ""
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

    def formatar_em_n_bits(self, binario, n):
        comprimento = len(binario)

        if n > comprimento:
            return "0" * (n - comprimento) + binario
        return binario

    # def split_mensagem(mensagem):
    #    mensagem[i:i + 4] for i in range(0, len(mensagem), 4)

    def definir_num_seq(self):
        if self.num_sequencia == 1:
            self.num_sequencia = 0
            return 0
        else:
            self.num_sequencia = 1
            return 1

    def enviar_mensagens(self):
        while True:
            try:
                mensagem = input('\n')
                pacotes_serializados = []
                msg_binario = "".join([self.formatar_em_n_bits(
                    bin(ord(caractere))[2:], 8) for caractere in mensagem])

                tamanho_da_mensagem = 32
                # mensagem_split = [mensagem[i:i + 4]
                # for i in range(0, len(mensagem), 4)]
                msg_binario_split = [msg_binario[i:i + tamanho_da_mensagem]
                                     for i in range(0, len(msg_binario), tamanho_da_mensagem)]
                # print(mensagem_split)
                # print(msg_binario_split)

                ultimo = 0
                for i in range(0, len(msg_binario_split)):
                    if i == len(msg_binario_split) - 1: ultimo = 1
                    segmento = Segmento(self.porta_de_origem, self.porta_de_destino, msg_binario_split[i], i % 2, "")
                    pacote = Pacote(self.ip_de_origem, self.ip_de_destino, segmento, ultimo)
                    pacote_serializado = pickle.dumps(pacote)
                    pacotes_serializados.append(pacote_serializado)
    
                
                for i in range(0, len(pacotes_serializados)):
                    ack = self.num_sequencia
                    while ack == self.num_sequencia: # envia enquanto o ack recebido != num seq enviado
                        self.cliente.send(pacotes_serializados[i])
                        time.sleep(1)
                        ack = self.receber_mensagens()

            except Exception as e:
                print(e)
                return

    def receber_mensagens(self):
        while True:
            try:
                pacote_serializado = self.cliente.recv(self.comprimento_do_buffer)
                pacote = pickle.loads(pacote_serializado)

                segmento = pacote.retornar_segmento()
                mensagem_recebida = segmento.retornar_mensagem()
                
                self.mensagem = self.mensagem + mensagem_recebida

                if pacote.is_ultimo():
                    self.mensagem = ""



                print(self.mensagem)
                return segmento.retornar_ack()

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.cliente.close()
                break
        
    def receber_porta_de_origem_do_servidor(self):
        while True:
            try:
                self.porta_de_origem = int(self.cliente.recv(
                    self.comprimento_do_buffer).decode())
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
