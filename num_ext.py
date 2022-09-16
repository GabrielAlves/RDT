import sys

MENOR_NUMERO_PERMITIDO = -999
MAIOR_NUMERO_PERMITIDO = 999

class NumExt:
    def __init__(self):
        self.dicionario_unidades_cardinal = {"1" : "um", "2" : "dois", "3" : "três", "4" : "quatro", "5" : "cinco", "6" : "seis", "7" : "sete", "8" : "oito", "9" : "nove"}
        self.dicionario_dezenas_cardinal = {"1" : {"0" : "dez", "1" : "onze", "2" : "doze", "3" : "treze", "4" : "catorze", "5" : "quinze", "6" : "dezesseis", "7" : "dezessete", "8" : "dezoito", "9" : "dezenove"}, "2" : "vinte", "3" : "trinta", "4" : "quarenta", "5" : "cinquenta", "6" : "sessenta", "7" : "setenta", "8" : "oitenta", "9" : "noventa"}
        self.dicionario_centenas_cardinal = {"1" : ["cem", "cento"], "2" : "duzentos", "3" : "trezentos", "4" : "quatrocentos", "5" : "quinhentos", "6" : "seiscentos", "7" : "setecentos", "8" : "oitocentos", "9" : "novecentos"}
        self.lista_posicoes_decimais_cardinal = [self.dicionario_unidades_cardinal, self.dicionario_dezenas_cardinal, self.dicionario_centenas_cardinal]
        
        self.dicionario_unidades_ordinal = {"1" : "primeiro", "2" : "segundo", "3" : "terceiro", "4" : "quarto", "5" : "quinto", "6" : "sexto", "7" : "sétimo", "8" : "oitavo", "9" : "nono"}
        self.dicionario_dezenas_ordinal = {"1" : "décimo", "2" : "vigésimo", "3" : "trigésimo", "4" : "quadragésimo", "5" : "quinquagésimo", "6" : "sexagésimo", "7" : "septuagésimo", "8" : "octogésimo", "9" : "nonagésimo"}
        self.dicionario_centenas_ordinal = {"1" : "centésimo", "2" : "ducentésimo", "3" : "trecentésimo", "4" : "quadringentésimo", "5" : "quinquentésimo", "6" : "sexcentésimo", "7" : "septingentésimo", "8" : "octingentésimo", "9" : "noningentésimo"}
        self.lista_posicoes_decimais_ordinal = [self.dicionario_unidades_ordinal, self.dicionario_dezenas_ordinal, self.dicionario_centenas_ordinal]

    def escrever_cardinal(self, numero):
        numero = str(numero)
        numero_cardinal = ""
        
        if numero[0] == "-":
            numero_cardinal += "Menos "
            numero = self.remover_sinal_negativo(numero)
            
        elif numero[0] == "0":
            numero_cardinal = "Zero"
            return numero_cardinal

        quantidade_algarismos = len(numero)
        indice_algarismo = 0

        while indice_algarismo < quantidade_algarismos:
            algarismo_atual = numero[indice_algarismo]
            indice_posicao_decimal = self.calcular_indice_posicao_decimal(indice_algarismo, quantidade_algarismos)
            dicionario_cardinal = self.selecionar_dicionario(self.lista_posicoes_decimais_cardinal, indice_posicao_decimal)

            # Se o algarismo atual está na casa das unidades
            if indice_posicao_decimal == 0:
                valor_por_extenso = dicionario_cardinal[algarismo_atual]
                numero_cardinal += valor_por_extenso

            # Se o algarismo atual está na casa das dezenas
            elif indice_posicao_decimal == 1:
                algarismo_sucessor = numero[indice_algarismo + 1]

                # Se o algarismo da dezena for 1, o valor recebe nomes especiais e o algarismo seguinte não influencia no nome. Ex : 11 é "Onze" e não "Dez e um"
                if algarismo_atual == "1":
                    valor_por_extenso = dicionario_cardinal[algarismo_atual][algarismo_sucessor]
                    numero_cardinal += valor_por_extenso
                    indice_algarismo += 2 # Um incremento para ir para o algarismo sucessor e outro para pula-lo(o algarismo sucessor já foi considerado no nome)
                    continue

                else:
                    
                    if algarismo_sucessor == "0":
                        valor_por_extenso = dicionario_cardinal[algarismo_atual]
                        numero_cardinal += valor_por_extenso
                        indice_algarismo += 2
                        continue

                    else:
                        valor_por_extenso = dicionario_cardinal[algarismo_atual]
                        numero_cardinal += valor_por_extenso
                        numero_cardinal += " e "

            # Se o algarismo atual está na casa das centenas
            else:
                algarismo_sucessor = numero[indice_algarismo + 1]
                algarismo_sucessor_do_sucessor = numero[indice_algarismo + 2]

                if algarismo_sucessor == "0" and algarismo_sucessor_do_sucessor == "0":

                    if algarismo_atual == "1":
                        valor_por_extenso = dicionario_cardinal[algarismo_atual][0] # Recebe "cem"
                        numero_cardinal += valor_por_extenso

                    else:
                        valor_por_extenso = dicionario_cardinal[algarismo_atual]
                        numero_cardinal += valor_por_extenso
                    
                    indice_algarismo += 3 # Um incrmeneto vai para o sucessor, outro vai para o sucessor do sucessor e o terceiro o pula
                    continue

                else:
                    
                    if algarismo_atual == "1":
                        valor_por_extenso = dicionario_cardinal[algarismo_atual][1] # Recebe "cento"

                    else:
                        valor_por_extenso = dicionario_cardinal[algarismo_atual]

                    valor_por_extenso += " e "
                    numero_cardinal += valor_por_extenso

                    # O algarismo sucessor é zero, mas o sucessor do sucessor não é
                    if algarismo_sucessor == "0":
                        indice_algarismo += 2
                        continue

                    else:
                        indice_algarismo += 1
                        continue

            indice_algarismo += 1

        numero_cardinal = self.tornar_inicial_maiuscula(numero_cardinal)
        
        return numero_cardinal

    def remover_sinal_negativo(self, numero):
        numero = numero[1:]
        return numero


    def escrever_ordinal(self, numero):
        if numero < 0:
            return "Não existe número ordinal para número negativo"

        elif numero == 0:
            return "Não existe número ordinal para zero"

        numero = str(numero)
        quantidade_algarismos = len(numero)
        numero_ordinal = ""

        for indice_algarismo in range(quantidade_algarismos):
            algarismo = numero[indice_algarismo]
            
            # Posições com zero não "recebem" nome e devem ser pulados na iteração. ex : 109 é centésimo nono(cenetena 1 - > "centésimo", dezena 0 -> "", unidade 9 -> "nono")
            if algarismo == "0": 
                continue

            indice_posicao_decimal = self.calcular_indice_posicao_decimal(indice_algarismo, quantidade_algarismos)
            dicionario_ordinal = self.selecionar_dicionario(self.lista_posicoes_decimais_ordinal, indice_posicao_decimal)
            valor_por_extenso = dicionario_ordinal[algarismo]

            numero_ordinal += valor_por_extenso

            if indice_algarismo != quantidade_algarismos - 1: 
                numero_ordinal += " "

        return numero_ordinal.capitalize()

    def calcular_indice_posicao_decimal(self, indice_algarismo, quantidade_algarismos):
        indice_posicao_decimal = ((quantidade_algarismos - 1) - indice_algarismo) % 3
        return indice_posicao_decimal

    def selecionar_dicionario(self, lista_posicoes_decimais, indice_posicao_decimal):
        dicionario = lista_posicoes_decimais[indice_posicao_decimal]
        return dicionario

    def tornar_inicial_maiuscula(self, numero_por_extenso):
        inicial_maiuscula = numero_por_extenso[0].upper()
        numero_sem_sua_inicial = numero_por_extenso[1:]
        numero_com_inicial_maiuscula = inicial_maiuscula + numero_sem_sua_inicial

        return numero_com_inicial_maiuscula