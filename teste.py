# Testando como gerar o checksum

def formatar_em_8_bits(binario):
    comprimento = len(binario)
    return "0" * (8 - comprimento) + binario

def retornar_complemento_de_1(binario):
    mapa = {"0" : "1", "1" : "0"}

    return "".join([mapa[bit] for bit in binario])

def main():
    mensagem = "hello world"
    mensagem_em_binario = "".join([formatar_em_8_bits(bin(ord(caractere))[2:]) for caractere in mensagem])

    # acrescenta 8 zeros no final se a palavra tiver um número impar de caracteres
    if len(mensagem_em_binario) % 16 != 0:
        mensagem_em_binario += "0" * 8

    print(mensagem_em_binario)
    print(retornar_complemento_de_1(mensagem_em_binario))

    soma = 0
    # Soma os 16 bits
    # for i in range(0, len(mensagem_em_binario), 16):
    #     soma += int(bin(int(mensagem_em_binario[i : i + 16], 2)), 2)
        
    #     # Se houver estouro, tirar o primeiro bit da soma e somar com o bit menos significativo
    #     if soma == 17:
    #         pass


if __name__ == "__main__":
    main()