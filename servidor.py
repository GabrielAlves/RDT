import threading
import socket
from queue import Queue


class Servidor:
    def __init__(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            servidor.bind(("127.0.0.1", 65432))
            servidor.listen()
            print('Servidor ligado')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        self.clientes = []
        self.fila_de_pacotes = Queue()
        thread = threading.Thread(target=self.tratar_pacotes_na_fila)
        thread.start()

        while True:
            cliente, endereco = servidor.accept()
            self.clientes.append(cliente)

            self.enviar_porta_de_origem_para_cliente(cliente)

            thread2 = threading.Thread(
                target=self.receber_pacote, args=[cliente])
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
                    self.enviar_para_todos(pacote)

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

    def enviar_para_todos(self, msg):
        for cliente in self.clientes:
            # if cliente != cliente_emissor:
            try:
                cliente.send(msg)
            except:
                self.remover_cliente(cliente)
                print('Removido:', cliente.getpeername())

    def remover_cliente(self, cliente):
        self.clientes.remove(cliente)
        print('Removido:', cliente.getpeername())
        self.listar_conectados()

    def listar_conectados(self):
        print('Conectados:')
        if self.clientes != []:
            for i in range(0, len(self.clientes)):
                print(self.clientes[i].getpeername())
        else:
            print('Ninguém')


if __name__ == "__main__":
    Servidor()
