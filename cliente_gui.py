import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
import socket
import threading
import pickle
import time
import sys
import json

from segmento import Segmento
from pacote import Pacote

from mensagem_de_usuario import MensagemDeUsuario
from mensagem_de_sistema import MensagemDeSistema
from config_cli_gui import ConfigCliGUI

class ClienteGUI:
    def __init__(self):
        self.criar_widgets()
        self.criar_atributos_de_cliente()

    def fazer_bind(self):
        try:
            self.cliente.bind((self.ip_de_origem, self.porta_de_origem))
            self.criar_threads_de_comunicacao()

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Não foi possível fazer o bind", exception)

    def atualizar_atributos_de_configuracao_na_classe(self):
        try:
            with open("json/config_cli.json", "r") as arquivo:
                dados_de_configuracao = json.load(arquivo) 

                self.ip_de_origem = dados_de_configuracao["ip_de_origem"]
                self.ip_de_destino = dados_de_configuracao["ip_de_destino"]
                self.porta_de_origem = dados_de_configuracao["porta_de_origem"]
                self.porta_de_destino = dados_de_configuracao["porta_de_destino"]
                self.ip_do_servidor = dados_de_configuracao["ip_do_servidor"]
                self.porta_do_servidor = dados_de_configuracao["porta_do_servidor"]

                MensagemDeSistema.criar_mensagem_de_sistema("info", "Sucesso", "Dados de configuração atualizados com sucesso na classe")

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Erro ao atualizar configurações", exception)

    def criar_atributos_de_cliente(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.comprimento_do_buffer = 10000000
        self.num_de_sequencia_atual = 0
        self.reenvio = False
        self.tempo_de_reenvio = 3
        self.mensagem_local = ""
        self.mensagem_remota = ""
        self.mensagem_de_usuario = MensagemDeUsuario(self.janela, self.canvas)

    def criar_threads_de_comunicacao(self):
        thread1 = threading.Thread(target=self.receber_mensagens)
        thread1.start()
    
    def criar_thread_de_mensagem_local(self):
        self.thread_de_mensagem_local = threading.Thread(target = self.criar_balao_de_mensagem_local)

    def criar_thread_de_mensagem_remota(self):
        self.thread_de_mensagem_remota = threading.Thread(target = self.criar_balao_de_mensagem_remoto)

    def atualizar_num_de_sequencia(self):
        self.num_de_sequencia_atual = 0 if self.num_de_sequencia_atual == 1 else 1

    def criar_widgets(self):
        self.criar_janela()
        self.criar_menu()
        self.criar_canvas()
        self.criar_frames()
        self.criar_widgets_de_interacao()

    def criar_janela(self):
        self.janela = tk.Tk()
        self.configurar_janela()
        
    def configurar_janela(self):
        self.janela.title("Chat")
        self.janela.geometry("400x400")
        self.janela.resizable(False, False)
        self.janela.iconbitmap(self.janela, "img/speech_bubble.ico")

    def criar_menu(self):
        self.criar_barra_de_menu()
        self.criar_item_de_configuracao()

    def criar_barra_de_menu(self):
        self.barra_de_menu = Menu(self.janela)
        self.janela.config(menu = self.barra_de_menu)

    def criar_item_de_configuracao(self):
        self.item_de_configuracao = Menu(self.barra_de_menu, tearoff = 0)
        self.item_de_configuracao.add_command(label = "Fazer bind", command = self.fazer_bind)
        self.item_de_configuracao.add_command(label = "Definir configurações", command = ConfigCliGUI)
        self.item_de_configuracao.add_command(label = "Atualizar configurações", command = self.atualizar_atributos_de_configuracao_na_classe)
        self.barra_de_menu.add_cascade(label = "Menu", menu = self.item_de_configuracao)

    def criar_frames(self):
        self.criar_frame1()
        self.criar_frame2()
        self.criar_frame3()

    def criar_canvas(self):
        self.canvas = tk.Canvas(self.janela)
        self.canvas.pack(fill = tk.BOTH, expand = True)

    def criar_frame1(self):
        self.frame1 = ttk.Frame(self.janela)
        self.frame1.pack(fill = tk.BOTH, expand = False, side = tk.BOTTOM)

    def criar_frame2(self):
        self.frame2 = ttk.Frame(self.frame1)
        self.frame2.grid(row = 0, column = 0, padx = 1, pady = 1)

    def criar_frame3(self):
        self.frame3 = ttk.Frame(self.frame1)
        self.frame3.grid(row = 0, column = 1, padx = 1, pady = 1)

    def criar_widgets_de_interacao(self):
        self.criar_caixa_de_texto()
        self.criar_botao_de_anexar_imagem()
        self.criar_botao_de_enviar()

    def criar_caixa_de_texto(self):
        self.caixa_de_texto = scrolledtext.ScrolledText(self.frame2, width = 33, height = 1, font = ("Arial", 12), wrap = tk.WORD)
        self.caixa_de_texto.grid()
        self.caixa_de_texto.focus()

    def criar_botao_de_anexar_imagem(self):
        self.botao_de_anexar_imagem = ttk.Button(self.frame3, text = "Anexar")
        self.botao_de_anexar_imagem.grid(row = 0)
        self.botao_de_anexar_imagem.config(state = "disabled")

    def criar_botao_de_enviar(self):
        self.botao_de_enviar = ttk.Button(self.frame3, text = "Enviar", command = self.enviar_mensagem)
        self.botao_de_enviar.grid(row = 1)

    def pegar_mensagem_da_caixa_de_texto(self):
        mensagem = self.caixa_de_texto.get("1.0", tk.END).strip()
        return mensagem

    def limpar_caixa_de_texto(self):
        self.caixa_de_texto.delete('1.0', tk.END)
        self.caixa_de_texto.focus()

    def enviar_mensagem(self):
        try:
            self.botao_de_enviar.config(state = "disabled")
            self.mensagem_local = self.pegar_mensagem_da_caixa_de_texto()
            self.limpar_caixa_de_texto()

            segmento = Segmento(self.porta_de_origem, self.porta_de_destino, self.mensagem_local, self.num_de_sequencia_atual, 0)
            pacote = Pacote(self.ip_de_origem, self.ip_de_destino, segmento)                
            pacote_serializado = pickle.dumps(pacote)

            self.cliente.sendto(pacote_serializado, (self.ip_do_servidor, self.porta_do_servidor))
            num_de_sequencia = self.num_de_sequencia_atual
            tempo_inicial = time.time()
            self.criar_thread_de_mensagem_local()
            self.thread_de_mensagem_local.start()

            # Enquanto o número de sequência atual não mudar, ainda não recebeu ACK. Continuar reenviando o pacote.
            while num_de_sequencia == self.num_de_sequencia_atual:
                
                # Temporizador
                if time.time() - tempo_inicial >= self.tempo_de_reenvio:
                    self.reenvio = True
                    tempo_inicial = time.time() # Reinicia temporizador

                if self.reenvio:
                    self.cliente.sendto(pacote_serializado, (self.ip_do_servidor, self.porta_do_servidor))
                    self.reenvio = False
            
            self.botao_de_enviar.config(state = "normal")

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Erro ao enviar mensagem", exception)
            # sys.exit()

    def receber_mensagens(self):
        while True:
            try:
                buffer = self.cliente.recvfrom(self.comprimento_do_buffer)
                print(buffer)
                print(type(buffer))
                pacote_serializado = buffer[0]
                pacote = pickle.loads(pacote_serializado)
            
                segmento = pacote.retornar_segmento()
                mensagem_recebida = segmento.retornar_mensagem()
                
                if mensagem_recebida:
                    self.mensagem_remota = mensagem_recebida
                    self.criar_thread_de_mensagem_remota()
                    self.thread_de_mensagem_remota.start()
                
                # # Se a mensagem não tiver conteúdo, é um ACK/NACK.
                elif mensagem_recebida == "" and segmento.retornar_ack() == 1:
                    # ack = segmento.retornar_ack()
                    num_de_sequencia = segmento.retornar_num_de_sequencia()
                    
                    # Chegou um ACK. Pacote recebido com sucesso. Mostrar mensagens do buffer e atualizar o número de sequência.
                    if self.num_de_sequencia_atual == num_de_sequencia:
                        # self.mensagem_gui.criar_balao_de_mensagem(self.mensagem_remota, False)
                        self.mensagem_remota = ""

                        self.atualizar_num_de_sequencia()

                    # Chegou um "NACK". Houve algum problema com o pacote. O pacote deve ser reenviado.
                    else:
                        self.reenvio = True

            except Exception as exception:
                MensagemDeSistema.criar_mensagem_de_sistema("error", "Não foi possível permanecer conectado no servidor", exception)
                # sys.exit()

    def criar_balao_de_mensagem_local(self):
        self.mensagem_de_usuario.criar_balao_de_mensagem(self.mensagem_local, True)

    def criar_balao_de_mensagem_remoto(self):
        self.mensagem_de_usuario.criar_balao_de_mensagem(self.mensagem_remota, False)

if __name__ == "__main__":
    ClienteGUI().janela.mainloop()