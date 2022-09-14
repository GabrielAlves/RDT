import threading
import socket
import pickle
import time

from pacote import Pacote
from segmento import Segmento

class Cliente:
    def __init__(self):
        self.ip_de_origem = socket.gethostbyname(socket.gethostname())
        self.ip_de_destino = "26.121.180.116" 
        # self.ip_de_destino = "26.138.96.133"  # Trocar pelo IP do outro cliente
        self.porta_de_origem = -1 # O servidor envia essa informação durante a conexão
        self.porta_de_destino = 65432
        

        self.comprimento_do_buffer = 10000
        self.num_de_sequencia_atual = 0
        self.reenvio = False
        self.tempo_de_reenvio = 3 # tempo em segundos

        self.mensagem = ""

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ip_do_servidor = "26.97.65.151"
        porta_do_servidor = 65432

        try:
            self.cliente.connect((ip_do_servidor, porta_do_servidor))

        except:
            return print('\nNão foi possívvel se conectar ao servidor!\n')

        # self.usuario = input('Usuário> ')
        print('\nConectado')

        self.receber_porta_de_origem_do_servidor()

        thread1 = threading.Thread(target=self.receber_mensagens)
        thread2 = threading.Thread(target=self.enviar_mensagens)
        thread1.start()
        thread2.start()

    def atualizar_num_de_sequencia(self):
        self.num_de_sequencia_atual = 0 if self.num_de_sequencia_atual == 1 else 1

    def enviar_mensagens(self):
        while True:
            try:
                mensagem = input('\n')
                # mensagem_em_binario = "".join([self.formatar_em_n_bits(bin(ord(caractere))[2:], 8) for caractere in mensagem])
                segmento = Segmento(self.porta_de_origem, self.porta_de_destino, mensagem, self.num_de_sequencia_atual, 0)
                pacote = Pacote(self.ip_de_origem, self.ip_de_destino, segmento)                
                pacote_serializado = pickle.dumps(pacote)

                self.cliente.send(pacote_serializado)
                num_de_sequencia = self.num_de_sequencia_atual
                tempo_inicial = time.time()

                # Enquanto o número de sequência atual não mudar, ainda não recebeu ACK. Continuar reenviando o pacote.
                while num_de_sequencia == self.num_de_sequencia_atual:
                    
                    # Temporizador
                    if time.time() - tempo_inicial >= self.tempo_de_reenvio:
                        self.reenvio = True
                        tempo_inicial = time.time() # Reinicia temporizador

                    if self.reenvio:
                        self.cliente.send(pacote_serializado)
                        self.reenvio = False

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

                if mensagem_recebida:
                    self.mensagem = mensagem_recebida

                # Se a mensagem não tiver conteúdo, é um ACK/NACK.
                else:
                    # ack = segmento.retornar_ack()
                    num_de_sequencia = segmento.retornar_num_de_sequencia()
                    
                    # Chegou um ACK. Pacote recebido com sucesso. Atualizar o número de sequência.
                    if self.num_de_sequencia_atual == num_de_sequencia:
                        
                        # Se já tiver alguma mensagem no "buffer" de mensagem
                        if self.mensagem != "":
                            print(self.mensagem)
                            self.mensagem = ""

                        self.atualizar_num_de_sequencia()

                    # Chegou um "NACK". Houve algum problema com o pacote. O pacote deve ser reenviado.
                    else:
                        self.reenvio = True

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
