import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import socket
import threading
import pickle
import time

from segmento import Segmento
from pacote import Pacote

from mensagem_gui import Mensagem

class ClienteGUI:
    def __init__(self):
        self.criar_widgets()
        self.criar_configuracoes_de_comunicacao()

    def criar_configuracoes_de_comunicacao(self):
        self.criar_atributos_de_cliente()
        self.estabelecer_conexao_com_servidor()
        self.receber_informacao_da_porta_de_origem()
        # self.criar_threads_de_comunicacao()

    def criar_atributos_de_cliente(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_de_origem = socket.gethostbyname(socket.gethostname())
        self.ip_de_destino = "26.209.24.137" # Trocar pelo IP do outro cliente
        self.porta_de_origem = -1 # O servidor envia essa informação durante a conexão
        self.porta_de_destino = 65432
        self.comprimento_do_buffer = 10000
        self.num_de_sequencia_atual = 0
        self.reenvio = False
        self.tempo_de_reenvio = 3
        self.mensagem = ""
        self.mensagem_gui = Mensagem(self.janela, self.canvas)

    def estabelecer_conexao_com_servidor(self):
        ip_do_servidor = "26.209.24.137"
        porta_do_servidor = 65432

        try:
            self.cliente.connect((ip_do_servidor, porta_do_servidor))

        except Exception as exception:
            print(exception)
            return print('\nNão foi possívvel se conectar ao servidor!\n')

        # self.usuario = input('Usuário> ')
        print('\nConectado')

    def criar_threads_de_comunicacao(self):
        thread1 = threading.Thread(target=self.receber_mensagens)
        thread1.start()

    def atualizar_num_de_sequencia(self):
        self.num_de_sequencia_atual = 0 if self.num_de_sequencia_atual == 1 else 1
        
    def receber_informacao_da_porta_de_origem(self):
        while True:
            try:
                self.porta_de_origem = int(self.cliente.recv(self.comprimento_do_buffer).decode())
                print(type(self.porta_de_origem))
                print(self.porta_de_origem)
                break

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.cliente.close()
                break

    def criar_widgets(self):
        self.criar_janela()
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
        # self.janela.config(bg = "lightgray")

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
        # self.frame2.grid_columnconfigure(0, weight = 1)

    def criar_frame3(self):
        self.frame3 = ttk.Frame(self.frame1)
        self.frame3.grid(row = 0, column = 1, padx = 1, pady = 1)
        # self.frame2.grid_columnconfigure(0, weight = 1)

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

    def criar_botao_de_enviar(self):
        self.botao_de_anexar_imagem = ttk.Button(self.frame3, text = "Enviar", command = self.enviar_mensagem)
        self.botao_de_anexar_imagem.grid(row = 1)

    def pegar_mensagem_da_caixa_de_texto(self):
        mensagem = self.caixa_de_texto.get("1.0", tk.END).strip()
        return mensagem

    def limpar_caixa_de_texto(self):
        self.caixa_de_texto.delete("1.0", tk.END)
        self.caixa_de_texto.focus()

    def enviar_mensagem(self):
        try:
            # self.limpar_caixa_de_texto()
            # self.caixa_de_texto.config(state = "disabled")
            mensagem = self.pegar_mensagem_da_caixa_de_texto()
            segmento = Segmento(self.porta_de_origem, self.porta_de_destino, mensagem, self.num_de_sequencia_atual, 0)
            pacote = Pacote(self.ip_de_origem, self.ip_de_destino, segmento)                
            pacote_serializado = pickle.dumps(pacote)

            self.mensagem_gui.criar_balao_de_mensagem(mensagem, True)

            # self.cliente.send(pacote_serializado)
            # num_de_sequencia = self.num_de_sequencia_atual
            # tempo_inicial = time.time()

            # # Enquanto o número de sequência atual não mudar, ainda não recebeu ACK. Continuar reenviando o pacote.
            # while num_de_sequencia == self.num_de_sequencia_atual:
                
            #     # Temporizador
            #     if time.time() - tempo_inicial >= self.tempo_de_reenvio:
            #         self.reenvio = True
            #         tempo_inicial = time.time() # Reinicia temporizador

            #     if self.reenvio:
            #         self.cliente.send(pacote_serializado)
            #         self.reenvio = False

            self.caixa_de_texto.config(state = "normal")

        except Exception as e:
            print(e)
            return

    def receber_mensagens(self):
        while True:
            try:
                pacote_serializado = self.cliente.recv(self.comprimento_do_buffer)
                pacote = pickle.loads(pacote_serializado)
            
                segmento = pacote.retornar_segmento()
                mensagem_recebida = segmento.retornar_mensagem()

                if mensagem_recebida:
                    self.mensagem = mensagem_recebida

                # Se a mensagem não tiver conteúdo, é um ACK/NACK.
                else:
                    # ack = segmento.retornar_ack()
                    num_de_sequencia = segmento.retornar_num_de_sequencia()
                    
                    # Chegou um ACK. Pacote recebido com sucesso. Atualizar o número de sequência.
                    if self.num_de_sequencia_atual == num_de_sequencia:
                        
                        # Se já tiver alguma mensagem no "buffer" de mensagem
                        if self.mensagem != "":
                            print(self.mensagem)
                            self.mensagem = ""

                        self.atualizar_num_de_sequencia()

                    # Chegou um "NACK". Houve algum problema com o pacote. O pacote deve ser reenviado.
                    else:
                        self.reenvio = True

            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.cliente.close()
                break

if __name__ == "__main__":
    ClienteGUI().janela.mainloop()