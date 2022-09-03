from operator import index
import threading
import socket
from queue import Queue
import pickle


class Servidor:
    def __init__(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            servidor.bind(("127.0.0.1", 65432))
            servidor.listen()
            print('Servidor ligado')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        self.clientes = {}
        self.fila_de_pacotes = Queue()
        thread = threading.Thread(target = self.tratar_pacotes_na_fila)
        thread.start()

        while True:
            cliente, endereco = servidor.accept()
            self.clientes[endereco[0]] = cliente

            self.enviar_porta_de_origem_para_cliente(cliente)

            thread2 = threading.Thread(target=self.receber_pacote, args=[cliente])
            thread2.start()

            self.listar_conectados()

    def enviar_porta_de_origem_para_cliente(self, cliente):
        porta = str(cliente.getpeername()[1])
        cliente.send(porta.encode())


    def tratar_pacotes_na_fila(self):
        while True:
            if not self.fila_de_pacotes.empty():
                pacote = self.fila_de_pacotes.get()
                print(f"O que fazer com a mensagem ")
                decisao = int(input(f"Corromper pacote?(1/0)"))

                if decisao == 1:
                    pass

                else:
                    self.enviar_pacote(pacote)

    def receber_pacote(self, cliente):
        while True:
            try:
                pacote = cliente.recv(10000)
                self.fila_de_pacotes.put(pacote)
                # print(f"mensagem {msg} colocada na fila")

                # self.enviar_para_todos(msg, cliente)
            except:
                self.remover_cliente(cliente)
                break

    def enviar_pacote(self, pacote_serializado):
        pacote = pickle.loads(pacote_serializado)
        ip_de_destino = pacote.retornar_ip_de_destino()

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
