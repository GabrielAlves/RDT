import threading
import socket
from queue import Queue


class Servidor:
    def __init__(self):
        self.clientes = []
        self.fila_de_mensagens = Queue()

        # thread2 = threading.Thread(target = self.tratar_mensagens_na_fila)
        # thread2.start()

        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            servidor.bind(("127.0.0.1", 65432))
            servidor.listen()
            print('Servidor ligado')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        while True:

            cliente, endereco = servidor.accept()

            self.clientes.append(cliente)

            thread1 = threading.Thread(
                target=self.tratar_mensagens, args=[cliente])
            thread1.start()

            self.listar_conectados()

    # def tratar_mensagens_na_fila(self):
    #     while not self.fila_de_mensagens.empty():
    #         mensagem = self.fila_de_mensagens.get()
    #         print(f"O que fazer com a mensagem {self.fila_de_mensagens.get()}")
    #         decisao = int(input(f"Corromper pacote?(1/0)"))

    #         if decisao == 1:
    #             pass

    #         else:
    #             pass

    def tratar_mensagens(self, cliente):
        while True:
            try:
                msg = cliente.recv(10000)
                self.fila_de_mensagens.put(msg)

                self.enviar_para_todos(msg, cliente)
            except:
                self.remover_cliente(cliente)
                break

    def enviar_para_todos(self, msg, cliente_emissor):
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
        else: print('Ninguém')


if __name__ == "__main__":
    Servidor()
