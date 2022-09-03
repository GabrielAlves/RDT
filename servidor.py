import threading
import socket
from queue import Queue
import pickle
from segmento import Segmento
from pacote import Pacote

class Servidor:
    def __init__(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nome_do_computador = socket.gethostname()
        self.ip = socket.gethostbyname(self.nome_do_computador)
        self.menu = '''O que fazer com a mensagem?
                  0 -> Envia a mensagem normalmente.
                  1 -> Corrompe pacote.
                  2 -> Não envia ACK de volta.    
                '''

        try:
            servidor.bind((self.ip, 65432))
            servidor.listen()
            print('Servidor ligado')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        self.clientes = {}
        # self.fila_de_pacotes = Queue()
        # thread = threading.Thread(target=self.tratar_pacotes_na_fila)
        # thread.start()

        while True:
            cliente, endereco = servidor.accept()
            self.clientes[endereco[0]] = cliente

            self.enviar_porta_de_origem_para_cliente(cliente)

            thread2 = threading.Thread(
                target=self.receber_pacote, args=[cliente])
            thread2.start()

            self.listar_conectados()

    def enviar_porta_de_origem_para_cliente(self, cliente):
        porta = str(cliente.getpeername()[1])
        cliente.send(porta.encode())

    def tratar_pacote(self, pacote):
        print(self.menu)
        decisao = int(input("O que fazer?:"))

        if decisao == 0:
            print("Pacote enviado com sucesso. 'ACK' pro cliente de origem")
            self.enviar_pacote(pacote)
            pacote = self.criar_ack(pacote)
            self.enviar_pacote(pacote)
    
        if decisao == 1:
            print("Pacote corrompido. 'NACK' enviado")
            pacote = self.corromper_pacote(pacote)
            # print("g1")
            pacote = self.criar_nack(pacote)
            self.enviar_pacote(pacote)
            # print("g2")

        else:
            pass


    def criar_nack(self, pacote):
        pacote = pickle.loads(pacote)
        ip_de_origem = self.ip
        ip_de_destino = pacote.retornar_ip_de_origem()

        segmento = pacote.retornar_segmento()
        porta_de_origem, porta_de_destino = segmento.retornar_porta_de_destino(), segmento.retornar_porta_de_origem()   
        num_de_sequencia = segmento.retornar_num_de_sequencia()
        ack = 0 if num_de_sequencia == 1 else 1
        segmento = Segmento(porta_de_origem, porta_de_destino, "", num_de_sequencia, ack)
        pacote = Pacote(ip_de_origem, ip_de_destino, segmento, 0)
        pacote = pickle.dumps(pacote)
        return pacote

    def criar_ack(self, pacote):
        pacote = pickle.loads(pacote)
        ip_de_origem = self.ip
        ip_de_destino = pacote.retornar_ip_de_origem()

        segmento = pacote.retornar_segmento()
        porta_de_origem, porta_de_destino = segmento.retornar_porta_de_destino(), segmento.retornar_porta_de_origem()   
        num_de_sequencia = segmento.retornar_num_de_sequencia()
        ack = num_de_sequencia
        segmento = Segmento(porta_de_origem, porta_de_destino, "", num_de_sequencia, ack)
        pacote = Pacote(ip_de_origem, ip_de_destino, segmento, 0)
        pacote = pickle.dumps(pacote)
        return pacote

    def corromper_pacote(self, pacote):
        pacote = pickle.loads(pacote)
        segmento = pacote.retornar_segmento()
        segmento.trocar_bit_na_mensagem()
        return pickle.dumps(pacote)



    def receber_pacote(self, cliente):
        while True:
            try:
                pacote = cliente.recv(10000)
                # self.fila_de_pacotes.put(pacote)
                self.tratar_pacote(pacote)
                # print(f"mensagem {msg} colocada na fila")

                # self.enviar_para_todos(msg, cliente)
            except:
                self.remover_cliente(cliente)
                break

    def enviar_pacote(self, pacote_serializado):
        pacote = pickle.loads(pacote_serializado)
        ip_de_destino = pacote.retornar_ip_de_destino()
        # print(self.clientes)
        cliente = self.clientes[ip_de_destino]

        cliente.send(pacote_serializado)

    # def selecionar_cliente(self, ip_de_destino, porta_de_de)


    # def enviar_para_todos(self, msg):
    #     for cliente in self.clientes:
    #         # if cliente != cliente_emissor:
    #         try:
    #             cliente.send(msg)
    #         except:
    #             self.remover_cliente(cliente)
    #             print('Removido:', cliente.getpeername())

    def remover_cliente(self, cliente):
        for endereco in self.clientes:
            if self.clientes[endereco] == cliente:
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
                print(self.clientes[endereco].getpeername())
        else: print('Ninguém')


if __name__ == "__main__":
    Servidor()
