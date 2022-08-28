class Pacote:
    def __init__(self, _ip_de_origem, _ip_de_destino, _segmento, _usuario):
        self.__ip_de_origem = _ip_de_origem
        self.__ip_de_destino = _ip_de_destino
        self.__segmento = _segmento
        self._usuario = _usuario

    def retornar_segmento(self):
        return self.__segmento

    def retornar_ip_de_origem(self):
        return self.__ip_de_origem
    
    def retornar_usuario(self):
        return self._usuario