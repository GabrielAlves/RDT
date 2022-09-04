import threading
import socket
import pickle

from segmento import Segmento
from pacote import Pacote

class Servidor:
    def __init__(self):
        self.ultimo_enviado = {}

        self.ip_do_servidor = socket.gethostbyname(socket.gethostname())
        self.porta_do_servidor = 65432
        self.comprimento_do_buffer = 10000

        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            servidor.bind((self.ip_do_servidor, self.porta_do_servidor))
            servidor.listen()
            print('Servidor ligado')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        self.clientes = {}

        while True:
            cliente, endereco = servidor.accept()
            self.clientes[endereco[0]] = cliente, None

            self.enviar_porta_de_origem_para_cliente(cliente)

            thread2 = threading.Thread(target=self.receber_pacote, args=[cliente])
            thread2.start()

            self.listar_conectados()

    def receber_pacote(self, cliente):
        while True:
            try:
                pacote_serializado = cliente.recv(self.comprimento_do_buffer)
                pacote = pickle.loads(pacote_serializado)
                self.tratar_pacote(pacote)
        
            except:
                self.remover_cliente(cliente)
                break

    def tratar_pacote(self, pacote):
        if not self.eh_pacote_repetido(pacote):
            decisao1 = int(input("Corromper pacote?(0 -> Não corromper; 1 -> Corromper):"))
            decisao2 = int(input("Enviar ACK/NACK de volta?(0 -> Não enviar; 1 -> Enviar)"))

            if decisao1 == 0:
                print("Pacote não foi corrompido.")
        
            elif decisao1 == 1:
                pacote = self.corromper_pacote(pacote)
                print("Pacote corrompido.")

            checksums_iguais = self.verificar_checksum(pacote)

            if checksums_iguais:
                reconhecimento = self.criar_pacote_de_reconhecimento(pacote, True)
                print("'ACK' criado.")
                self.enviar_pacote(pacote)
                print("Pacote enviado pro outro cliente.")

            else:
                reconhecimento = self.criar_pacote_de_reconhecimento(pacote, False)
                print("'NACK' criado.")

            if decisao2 == 0:
                print("Reconhecimento não foi enviado.")

            elif decisao2 == 1:
                self.enviar_pacote(reconhecimento)
                print("Reconhecimento enviado.")
            
            if decisao1 == 0 and decisao2 == 1:
                self.salvar_ultimo_enviado(pacote)

    def enviar_pacote(self, pacote):
        ip_de_destino = pacote.retornar_ip_de_destino()
        cliente = self.clientes[ip_de_destino][0]
        pacote_serializado = pickle.dumps(pacote)
        
        cliente.send(pacote_serializado)

    def eh_pacote_repetido(self, pacote):
        segmento = pacote.retornar_segmento()
        num_de_sequencia = segmento.retornar_num_de_sequencia()
        ip_de_origem = pacote.retornar_ip_de_origem()

        ultimo_pacote_enviado = self.clientes.get(ip_de_origem)[1]

        if ultimo_pacote_enviado != None:
            ultimo_segmento = ultimo_pacote_enviado.retornar_segmento()
            ultimo_num_de_sequencia = ultimo_segmento.retornar_num_de_sequencia()

            return ultimo_num_de_sequencia == num_de_sequencia

    def salvar_ultimo_enviado(self, pacote):
        ip_de_origem = pacote.retornar_ip_de_origem()
        self.clientes[ip_de_origem] = self.clientes[ip_de_origem][0], pacote


    def verificar_checksum(self, pacote):
        segmento = pacote.retornar_segmento()
        checksum_do_segmento = segmento.retornar_checksum()
        checksum_calculado = segmento.calcular_checksum(segmento.retornar_mensagem())

        return checksum_do_segmento == checksum_calculado


    def criar_pacote_de_reconhecimento(self, pacote, eh_ack):
        segmento = pacote.retornar_segmento()
        ip_de_destino = pacote.retornar_ip_de_origem()
        porta_de_origem, porta_de_destino = segmento.retornar_porta_de_destino(), segmento.retornar_porta_de_origem()   
        num_de_sequencia = segmento.retornar_num_de_sequencia()
        mensagem = ""
        
        if eh_ack:
            ack = num_de_sequencia

        else:
            ack = 0 if num_de_sequencia == 1 else 1

        segmento = Segmento(porta_de_origem, porta_de_destino, mensagem, num_de_sequencia, ack)
        pacote = Pacote(self.ip_do_servidor, ip_de_destino, segmento)
        return pacote

    def corromper_pacote(self, pacote):
        segmento = pacote.retornar_segmento()
        segmento.trocar_bit_na_mensagem()
        return pacote


    def remover_cliente(self, cliente):
        for endereco in self.clientes:
            if self.clientes[endereco][0] == cliente:
                chave = endereco
                break

        if chave != None:
            del self.clientes[endereco]
            print('Removido:', cliente.getpeername())
            self.listar_conectados()

    def listar_conectados(self):
        print('Conectados:')
        if self.clientes != []:
            for endereco in self.clientes:
                print(self.clientes[endereco][0].getpeername())
        else: print('Ninguém')

    def enviar_porta_de_origem_para_cliente(self, cliente):
        porta = str(cliente.getpeername()[1])
        cliente.send(porta.encode())


if __name__ == "__main__":
    Servidor()
