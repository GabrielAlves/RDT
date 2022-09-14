import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import pickle
import time

from pacote import Pacote
from segmento import Segmento

from num_ext import NumExt

class ServidorGUI:
    def __init__(self):
        self.criar_widgets()
        self.criar_configuracoes_de_comunicacao()

    def criar_configuracoes_de_comunicacao(self):
        self.criar_atributos_do_servidor()
        self.ligar_servidor()
        self.criar_threads_de_comunicacao()
        # self.aceitar_conexoes()

    def criar_atributos_do_servidor(self):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = {}
        self.ip_do_servidor = socket.gethostbyname(socket.gethostname())
        self.porta_do_servidor = 65432
        self.ultimo_enviado = {}
        self.comprimento_do_buffer = 10000
        self.contador_de_pacotes = 1
        self.travamento_de_pacotes = True
        self.pacote = None
        self.escritor_de_numeros = NumExt()

    def criar_threads_de_comunicacao(self):
        thread1 = threading.Thread(target=self.aceitar_conexoes)
        thread1.start()

    def ligar_servidor(self):
        try:
            self.servidor.bind((self.ip_do_servidor, self.porta_do_servidor))
            self.servidor.listen()
            print('Servidor ligado')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')
        
    def aceitar_conexoes(self):
        while True:
            cliente, endereco = self.servidor.accept()
            self.clientes[endereco[0]] = cliente, None

            self.enviar_porta_de_origem_para_cliente(cliente)

            thread2 = threading.Thread(target=self.receber_pacote, args=[cliente])
            thread2.start()
            # self.listar_conectados()

    def enviar_porta_de_origem_para_cliente(self, cliente):
        porta = str(cliente.getpeername()[1])
        cliente.send(porta.encode())

    def receber_pacote(self, cliente):
        while True:
            try:
                pacote_serializado = cliente.recv(self.comprimento_do_buffer)
                pacote = pickle.loads(pacote_serializado)
                self.mostrar_informacoes_do_pacote(pacote)
        
            except:
                # self.remover_cliente(cliente)
                break

    def preencher_campos(self, pacote):
        segmento = pacote.retornar_segmento()
        ip_de_origem = pacote.retornar_ip_de_origem()
        ip_de_destino = pacote.retornar_ip_de_destino()
        porta_de_origem = segmento.retornar_porta_de_origem()
        porta_de_destino = segmento.retornar_porta_de_destino()
        comprimento = segmento.retornar_comprimento()
        checksum = segmento.retornar_checksum()
        mensagem = segmento.retornar_mensagem()

        self.inserir_texto_no_campo(self.campo_do_ip_de_origem, ip_de_origem)
        self.inserir_texto_no_campo(self.campo_do_ip_de_destino, ip_de_destino)
        self.inserir_texto_no_campo(self.campo_da_porta_de_origem, porta_de_origem)
        self.inserir_texto_no_campo(self.campo_da_porta_de_destino, porta_de_destino)
        self.inserir_texto_no_campo(self.campo_do_comprimento_do_segmento, comprimento)
        self.inserir_texto_no_campo(self.campo_do_checksum, checksum)

        self.inserir_mensagem_no_campo(mensagem)

    def inserir_texto_no_campo(self, campo, texto):
        campo.configure(state = "normal")
        campo.insert(0, texto)
        campo.configure(state = "readonly")

    def inserir_mensagem_no_campo(self, mensagem):
        self.campo_da_mensagem.configure(state = "normal")
        self.campo_da_mensagem.insert("1.0", mensagem)
        self.campo_da_mensagem.configure(state = "disabled")

    def inserir_mensagem_de_log(self, mensagem):
        self.campo_de_log.configure(state = "normal")        
        self.campo_de_log.insert(tk.END, f"{mensagem}\n")
        self.campo_de_log.configure(state = "disabled")

    def limpar_campos(self):
        self.limpar_texto_no_campo(self.campo_do_ip_de_origem)
        self.limpar_texto_no_campo(self.campo_do_ip_de_destino)
        self.limpar_texto_no_campo(self.campo_da_porta_de_origem)
        self.limpar_texto_no_campo(self.campo_da_porta_de_destino)
        self.limpar_texto_no_campo(self.campo_do_comprimento_do_segmento)
        self.limpar_texto_no_campo(self.campo_do_checksum)
        self.limpar_campo_de_mensagem()

    def limpar_texto_no_campo(self, campo):
        campo.configure(state = "normal")
        campo.delete(0, tk.END)
        campo.configure(state = "readonly")

    def limpar_campo_de_mensagem(self):
        self.campo_da_mensagem.configure(state = "normal")
        self.campo_da_mensagem.delete("1.0", tk.END)
        self.campo_da_mensagem.configure(state = "disabled")

    def mostrar_informacoes_do_pacote(self, pacote):
        if not self.eh_pacote_repetido(pacote):
            self.travamento_de_pacotes = True
            self.pacote = pacote
            self.preencher_campos(pacote)
            
            while self.travamento_de_pacotes:
                pass

    def processar_pacote(self, pacote):
        self.inserir_mensagem_de_log(f"{self.escritor_de_numeros.escrever_ordinal(self.contador_de_pacotes)} pacote")
        self.contador_de_pacotes += 1
        self.inserir_mensagem_de_log("-" * 48)

        if self.decisao_de_corrompimento.get() == 0: 
            self.inserir_mensagem_de_log("Pacote não foi corrompido")

        elif self.decisao_de_corrompimento.get() == 1:
            pacote = self.corromper_pacote(pacote)
            self.inserir_mensagem_de_log("Pacote corrompido")

        checksum_iguais = self.verificar_checksum(pacote)

        if checksum_iguais:
            reconhecimento = self.criar_pacote_de_reconhecimento(pacote, True)
            self.inserir_mensagem_de_log("'ACK' criado.")

        else:
            reconhecimento = self.criar_pacote_de_reconhecimento(pacote, False)
            self.inserir_mensagem_de_log("'NACK' criado.")

        if self.decisao_da_perda_de_ack.get() == 0:
            self.enviar_pacote(reconhecimento)
            self.enviar_pacote(pacote)
            self.inserir_mensagem_de_log("Pacote enviado pro outro cliente.")
            self.inserir_mensagem_de_log("Reconhecimento enviado.")

        elif self.decisao_da_perda_de_ack.get() == 1:
            self.inserir_mensagem_de_log("Reconhecimento não foi enviado.")
        
        if self.decisao_de_corrompimento.get() == 0 and self.decisao_da_perda_de_ack.get() == 0:
            self.salvar_ultimo_enviado(pacote)

        self.inserir_mensagem_de_log("-" * 48)

        self.limpar_campos()
        self.travamento_de_pacotes = False
        self.pacote = None



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
        
        # se nack
        if not eh_ack:
            num_de_sequencia = 0 if num_de_sequencia == 1 else 1

        segmento = Segmento(porta_de_origem, porta_de_destino, mensagem, num_de_sequencia, 1)
        pacote = Pacote(self.ip_do_servidor, ip_de_destino, segmento)
        return pacote

    def corromper_pacote(self, pacote):
        segmento = pacote.retornar_segmento()
        segmento.trocar_bit_na_mensagem()
        return pacote

    def inicializar_variaveis_do_radiobutton(self):
        self.decisao_de_corrompimento = tk.IntVar()
        self.decisao_da_perda_de_ack = tk.IntVar()

        self.decisao_de_corrompimento.set(0)
        self.decisao_da_perda_de_ack.set(0)

    def criar_widgets(self):
        self.criar_janela()
        self.criar_frames()
        self.criar_widgets_dos_frames()
        # self.criar_widgets_do_frame2()

    def criar_janela(self):
        self.janela = tk.Tk()
        self.configurar_janela()
        
        
    def configurar_janela(self):
        self.janela.title("Monitoramento")
        self.janela.config(width = 300)
        self.janela.resizable(False, False)
        self.janela.columnconfigure(0, weight = 1)
        self.janela.iconbitmap(self.janela, "img/engine.ico")
        # self.janela.config(bg = "lightgray")

    def criar_frames(self):
        self.criar_frame1()
        self.criar_frame2()
        self.criar_frame3()
        self.criar_frame4()
        self.criar_frame5()
        self.criar_frame6()

    def criar_frame1(self):
        self.frame1 = ttk.Frame(self.janela)
        self.frame1.pack(pady = 3)
        # self.frame1.grid(row = 0)

    def criar_frame2(self):
        self.frame2 = ttk.Frame(self.janela)
        self.frame2.pack(pady = 3)
        # self.frame2.grid(row = 1)

    def criar_frame3(self):
        self.frame3 = ttk.Frame(self.janela)
        self.frame3.pack(pady = 3)
        # self.frame3.grid(row = 2)

    def criar_frame4(self):
        self.frame4 = ttk.Frame(self.janela)
        self.frame4.pack(pady = 3)
        # self.frame4.grid(row = 3)
    
    def criar_frame5(self):
        self.frame5 = ttk.Frame(self.janela)
        self.frame5.pack(pady = 3)
        # self.frame5.grid(row = 4)

    def criar_frame6(self):
        self.frame6 = ttk.Frame(self.janela)
        self.frame6.pack(pady = 3)
        

    def criar_widgets_do_frame1(self):
        self.criar_label_do_ip_de_origem()
        self.criar_campo_do_ip_de_origem()
        self.criar_label_do_ip_de_destino()
        self.criar_campo_do_ip_de_destino()
        
    def criar_widgets_do_frame2(self):
        self.criar_label_da_porta_de_origem()
        self.criar_campo_da_porta_de_origem()
        self.criar_label_da_porta_de_destino()
        self.criar_campo_da_porta_de_destino()

    def criar_widgets_do_frame3(self):
        self.criar_label_do_comprimento_do_segmento()
        self.criar_campo_do_comprimento_do_segmento()
        self.criar_label_do_checksum()
        self.criar_campo_do_checksum()

    def criar_widgets_do_frame4(self):
        self.criar_label_da_mensagem()
        self.criar_campo_da_mensagem()

    def criar_widgets_do_frame5(self):
        self.inicializar_variaveis_do_radiobutton()
        self.criar_radiobutton_do_nao_corrompimento()
        self.criar_radiobutton_do_corrompimento()
        self.criar_radiobutton_da_nao_perda_de_ack()
        self.criar_radiobutton_da_perda_de_ack()
        self.criar_botao_de_processar()

    def criar_widgets_do_frame6(self):
        self.criar_label_do_log()
        self.criar_campo_de_log()

    def criar_widgets_dos_frames(self):
        self.criar_widgets_do_frame1()
        self.criar_widgets_do_frame2()
        self.criar_widgets_do_frame3()
        self.criar_widgets_do_frame4()
        self.criar_widgets_do_frame5()
        self.criar_widgets_do_frame6()

    def criar_label_do_ip_de_origem(self):
        self.label_do_ip_de_origem = ttk.Label(self.frame1, text = "IP de origem", font = ("Arial", 12))
        self.label_do_ip_de_origem.grid(row = 0, column = 0, padx = 3)  

    def criar_campo_do_ip_de_origem(self):
        self.campo_do_ip_de_origem = ttk.Entry(self.frame1)
        self.campo_do_ip_de_origem.grid(row = 1, column = 0, padx = 3)
        self.campo_do_ip_de_origem.configure(state = "readonly")

    def criar_label_do_ip_de_destino(self):
        self.label_do_ip_de_destino = ttk.Label(self.frame1, text = "IP de destino", font = ("Arial", 12))
        self.label_do_ip_de_destino.grid(row = 0, column = 1, padx = 3)

    def criar_campo_do_ip_de_destino(self):
        self.campo_do_ip_de_destino = ttk.Entry(self.frame1)
        self.campo_do_ip_de_destino.grid(row = 1, column = 1, padx = 3)
        self.campo_do_ip_de_destino.configure(state = "readonly")

    def criar_label_da_porta_de_origem(self):
        self.label_da_porta_de_origem = ttk.Label(self.frame2, text = "Porta de origem", font = ("Arial", 12))
        self.label_da_porta_de_origem.grid(row = 0, column = 0, padx = 3)

    def criar_campo_da_porta_de_origem(self):
        self.campo_da_porta_de_origem = ttk.Entry(self.frame2)
        self.campo_da_porta_de_origem.grid(row = 1, column = 0, padx = 3)
        self.campo_da_porta_de_origem.configure(state = "readonly")

    def criar_label_da_porta_de_destino(self):
        self.label_da_porta_de_destino = ttk.Label(self.frame2, text = "Porta de destino", font = ("Arial", 12))
        self.label_da_porta_de_destino.grid(row = 0, column = 1, padx = 3)

    def criar_campo_da_porta_de_destino(self):
        self.campo_da_porta_de_destino = ttk.Entry(self.frame2)
        self.campo_da_porta_de_destino.grid(row = 1, column = 1, padx = 3)
        self.campo_da_porta_de_destino.config(state = "readonly")

    def criar_label_do_comprimento_do_segmento(self):
        self.label_do_comprimento_do_segmento = ttk.Label(self.frame3, text = "Comprimento", font = ("Arial", 12))
        self.label_do_comprimento_do_segmento.grid(row = 0, column = 0, padx = 3)

    def criar_campo_do_comprimento_do_segmento(self):
        self.campo_do_comprimento_do_segmento = ttk.Entry(self.frame3)
        self.campo_do_comprimento_do_segmento.grid(row = 1, column = 0, padx = 3)
        self.campo_do_comprimento_do_segmento.config(state = "readonly")

    def criar_label_do_checksum(self):
        self.label_do_checksum = ttk.Label(self.frame3, text = "Checksum", font = ("Arial", 12))
        self.label_do_checksum.grid(row = 0, column = 1, padx = 3)

    def criar_campo_do_checksum(self):
        self.campo_do_checksum = ttk.Entry(self.frame3)
        self.campo_do_checksum.grid(row = 1, column = 1, padx = 3)
        self.campo_do_checksum.config(state = "readonly")

    def criar_label_da_mensagem(self):
        self.label_da_mensagem = ttk.Label(self.frame4, text = "Mensagem", font = ("Arial", 12))
        self.label_da_mensagem.grid(row = 0, columnspan = 2)

    def criar_campo_da_mensagem(self):
        self.campo_da_mensagem = scrolledtext.ScrolledText(self.frame4, width = 27, height = 1, font = ("Arial", 12), wrap = tk.WORD)
        self.campo_da_mensagem.grid(row = 1, column = 0, columnspan = 2)
        self.campo_da_mensagem.config(state = "disabled")

    def criar_radiobutton_do_nao_corrompimento(self):
        self.radiobutton_do_nao_corrompimento = ttk.Radiobutton(self.frame5, text = "Não corromper pacote", variable = self.decisao_de_corrompimento, value = 0)
        self.radiobutton_do_nao_corrompimento.grid(row = 0, column = 0, sticky = tk.W)

    def criar_radiobutton_do_corrompimento(self):
        self.radiobutton_do_corrompimento = ttk.Radiobutton(self.frame5, text = "Corromper pacote", variable = self.decisao_de_corrompimento, value = 1)
        self.radiobutton_do_corrompimento.grid(row = 1, column = 0, sticky = tk.W)

    def criar_radiobutton_da_nao_perda_de_ack(self):
        self.radiobutton_da_nao_perda_de_ack = ttk.Radiobutton(self.frame5, text = "Não perder ACK/NACK", variable = self.decisao_da_perda_de_ack,value = 0)
        self.radiobutton_da_nao_perda_de_ack.grid(row = 0, column = 1, sticky = tk.W)

    def criar_radiobutton_da_perda_de_ack(self):
        self.radiobutton_da_perda_de_ack = ttk.Radiobutton(self.frame5, text = "Perder ACK/NACK", variable = self.decisao_da_perda_de_ack, value = 1)
        self.radiobutton_da_perda_de_ack.grid(row = 1, column = 1, sticky = tk.W)

    def criar_botao_de_processar(self):
        self.botao_de_processar = ttk.Button(self.frame5, text = "Processar", command = lambda : self.processar_pacote(self.pacote))
        self.botao_de_processar.grid(row = 0, column = 2, rowspan = 2)

    def criar_label_do_log(self):
        self.label_do_log = ttk.Label(self.frame6, text = "Log", font = ("Arial", 12))
        self.label_do_log.grid(row = 0, columnspan = 2, padx = 3)

    def criar_campo_de_log(self):
        self.campo_de_log = scrolledtext.ScrolledText(self.frame6, width = 27, height = 5, font = ("Arial", 12), wrap = tk.WORD)
        self.campo_de_log.grid(columnspan = 2, pady = 3)
        self.campo_de_log.config(state = "disabled")
    

if __name__ == "__main__":
    ServidorGUI().janela.mainloop()