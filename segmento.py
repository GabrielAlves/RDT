class Segmento:
    def __init__(self, _porta_de_origem, _porta_de_destino, _mensagem, _num_de_sequencia, _ack):
        self.__porta_de_origem = _porta_de_origem
        self.__porta_de_destino = _porta_de_destino
        self.__mensagem = _mensagem
        self.__comprimento = 8 + self.contar_bytes_da_mensagem(_mensagem)
        self.__checksum = self.calcular_checksum(_mensagem)
        self.__ack = _ack
        self.num_de_sequencia = _num_de_sequencia

    def trocar_bit_na_mensagem(self):
        bit_trocado = "0" if self.__mensagem[-1] == "1" else "1"
        self.__mensagem = self.__mensagem[:-1] + bit_trocado

    def contar_bytes_da_mensagem(self, mensagem):
        return len(mensagem.encode("utf-8"))

    def retornar_comprimento(self):
        return self.__comprimento

    def retornar_mensagem(self):
        return self.__mensagem

    def retornar_porta_de_destino(self):
        return self.__porta_de_destino

    def retornar_porta_de_origem(self):
        return self.__porta_de_origem

    def retornar_checksum(self):
        return self.__checksum

    def retornar_ack(self):
        return self.__ack

    def formatar_em_n_bits(self, binario, n):
        comprimento = len(binario)

        if n > comprimento:
            return "0" * (n - comprimento) + binario
        return binario

    def retornar_complemento_de_1(self, binario):
        mapa = {"0": "1", "1": "0"}

        return "".join([mapa[bit] for bit in binario])

    def formar_cadeia_de_bits(self, mensagem):
        mensagem_em_binario = "".join([self.formatar_em_n_bits(
            bin(ord(caractere))[2:], 8) for caractere in mensagem])

        # acrescenta 8 zeros no final se a palavra tiver um número impar de caracteres
        if len(mensagem_em_binario) % 16 != 0:
            mensagem_em_binario += "00000000"

        return mensagem_em_binario

    def somar_blocos_de_16_bits(self, mensagem_em_binario):
        soma = 0

        # Soma blocos de 16 em 16 bits
        for i in range(0, len(mensagem_em_binario), 16):
            soma += int(mensagem_em_binario[i: i + 16], 2)

            # # Se houver estouro, tirar o primeiro bit da soma e somá-lo com o bit menos significativo
            if len(bin(soma)[2:]) == 17:
                soma = int(bin(soma)[3:], 2) + 1

        return soma

    def calcular_checksum(self, mensagem):
        mensagem_em_binario = self.formar_cadeia_de_bits(mensagem)
        soma = self.somar_blocos_de_16_bits(mensagem_em_binario)
        soma = self.formatar_em_n_bits(bin(soma)[2:], 16)
        complemento = self.retornar_complemento_de_1(soma)
        return complemento
