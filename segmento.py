class Segmento:
    def __init__(self, _porta_de_origem, _porta_de_destino, _mensagem):
        self.__porta_de_origem = _porta_de_origem
        self.__porta_de_destino = _porta_de_destino
        self.__mensagem = _mensagem
        self.__comprimento = 8 + self.contar_bytes_da_mensagem(_mensagem)
        self.__checksum = self.contar_bytes_da_mensagem(_mensagem) # Não é o checksum verdadeiro. Fins de teste
        # self.ack = # passar como argumento

    def contar_bytes_da_mensagem(self, mensagem):
        return len(mensagem.encode("utf-8"))

    def retornar_mensagem(self):
        return self.__mensagem