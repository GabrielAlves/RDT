import tkinter as tk
from tkinter import ttk
import json

from mensagem_de_sistema import MensagemDeSistema

class ConfigCliGUI:
    def __init__(self):
        self.criar_widgets()
        self.mostrar_dados_de_configuracao()

    def mostrar_dados_de_configuracao(self):
        try:
            with open("json/config_cli.json", "r") as arquivo:
                dados_de_configuracao = json.load(arquivo) 
                self.preencher_campos(dados_de_configuracao)

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Erro ao ler arquivo de configurações", exception)

    def preencher_campos(self, dados_de_configuracao):
        ip_de_origem = dados_de_configuracao["ip_de_origem"]
        ip_de_destino = dados_de_configuracao["ip_de_destino"]
        porta_de_origem = dados_de_configuracao["porta_de_origem"]
        porta_de_destino = dados_de_configuracao["porta_de_destino"]
        ip_do_servidor = dados_de_configuracao["ip_do_servidor"]
        porta_do_servidor = dados_de_configuracao["porta_do_servidor"]

        self.inserir_texto_no_campo(self.campo_do_ip_de_origem, ip_de_origem)
        self.inserir_texto_no_campo(self.campo_do_ip_de_destino, ip_de_destino)
        self.inserir_texto_no_campo(self.campo_da_porta_de_origem, porta_de_origem)
        self.inserir_texto_no_campo(self.campo_da_porta_de_destino, porta_de_destino)
        self.inserir_texto_no_campo(self.campo_do_ip_do_servidor, ip_do_servidor)
        self.inserir_texto_no_campo(self.campo_da_porta_do_servidor, porta_do_servidor)

    def inserir_texto_no_campo(self, campo, texto):
        campo.insert(0, texto)

    def criar_widgets(self):
        self.criar_janela()
        self.criar_frames()
        self.criar_widgets_dos_frames()

    def criar_janela(self):
        self.janela = tk.Tk()
        self.configurar_janela()
        
    def configurar_janela(self):
        self.janela.title("Configurações")
        self.janela.config(width = 300)
        self.janela.resizable(False, False)
        self.janela.iconbitmap(self.janela, "img/engine.ico")
        # self.janela.columnconfigure(0, weight = 1)

    def criar_frames(self):
        self.criar_frame1()
        self.criar_frame2()
        self.criar_frame3()
        self.criar_frame4()
    
    def criar_frame1(self):
        self.frame1 = ttk.Frame(self.janela)
        self.frame1.pack(fill = tk.BOTH, expand = True)
        # self.frame1.columnconfigure(1, weight = 1)
        # self.frame1.grid(row = 0)

    def criar_frame2(self):
        self.frame2 = ttk.Frame(self.janela)
        self.frame2.pack(fill = tk.BOTH, expand = True)
        # self.frame2.grid(row = 1)

    def criar_frame3(self):
        self.frame3 = ttk.Frame(self.janela)
        self.frame3.pack(fill = tk.BOTH, expand = True)
        # self.frame2.grid(row = 1)

    def criar_frame4(self):
        self.frame4 = ttk.Frame(self.janela)
        self.frame4.pack(fill = tk.BOTH, expand = True)
        # self.frame2.grid(row = 1)

    def criar_widgets_dos_frames(self):
        self.criar_widgets_do_frame1()
        self.criar_widgets_do_frame2()
        self.criar_widgets_do_frame3()
        self.criar_widgets_do_frame4()

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
        self.criar_label_do_ip_do_servidor()
        self.criar_campo_do_ip_do_servidor()
        self.criar_label_da_porta_do_servidor()
        self.criar_campo_da_porta_do_servidor()

    def criar_widgets_do_frame4(self):
        self.criar_botao_de_salvar()

    def criar_label_do_ip_de_origem(self):
        self.label_do_ip_de_origem = ttk.Label(self.frame1, text = "IP de origem", font = ("Arial", 12))
        self.label_do_ip_de_origem.grid(row = 0, column = 0, padx = 3, pady = 2)  

    def criar_campo_do_ip_de_origem(self):
        self.campo_do_ip_de_origem = ttk.Entry(self.frame1)
        self.campo_do_ip_de_origem.grid(row = 0, column = 1, padx = 3, pady = 2, sticky = tk.NSEW)
        self.campo_do_ip_de_origem.focus()

    def criar_label_do_ip_de_destino(self):
        self.label_do_ip_de_destino = ttk.Label(self.frame1, text = "IP de destino", font = ("Arial", 12))
        self.label_do_ip_de_destino.grid(row = 1, column = 0, padx = 3, pady = 2)

    def criar_campo_do_ip_de_destino(self):
        self.campo_do_ip_de_destino = ttk.Entry(self.frame1)
        self.campo_do_ip_de_destino.grid(row = 1, column = 1, padx = 3, pady = 2)

    def criar_label_da_porta_de_origem(self):
        self.label_da_porta_de_origem = ttk.Label(self.frame2, text = "Porta de origem", font = ("Arial", 12))
        self.label_da_porta_de_origem.grid(row = 0, column = 0, padx = 3, pady = 2)

    def criar_campo_da_porta_de_origem(self):
        self.campo_da_porta_de_origem = ttk.Entry(self.frame2)
        self.campo_da_porta_de_origem.grid(row = 0, column = 1, padx = 3, pady = 2)

    def criar_label_da_porta_de_destino(self):
        self.label_da_porta_de_destino = ttk.Label(self.frame2, text = "Porta de destino", font = ("Arial", 12))
        self.label_da_porta_de_destino.grid(row = 1, column = 0, padx = 3, pady = 2)

    def criar_campo_da_porta_de_destino(self):
        self.campo_da_porta_de_destino = ttk.Entry(self.frame2)
        self.campo_da_porta_de_destino.grid(row = 1, column = 1, padx = 3, pady = 2)

    def criar_label_do_ip_do_servidor(self):
        self.label_do_ip_do_servidor = ttk.Label(self.frame3, text = "IP do servidor", font = ("Arial", 12))
        self.label_do_ip_do_servidor.grid(row = 0, column = 0, padx = 3, pady = 2)

    def criar_campo_do_ip_do_servidor(self):
        self.campo_do_ip_do_servidor = ttk.Entry(self.frame3)
        self.campo_do_ip_do_servidor.grid(row = 0, column = 1, padx = 3, pady = 2)

    def criar_label_da_porta_do_servidor(self):
        self.label_da_porta_do_servidor = ttk.Label(self.frame3, text = "Porta do servidor", font = ("Arial", 12))
        self.label_da_porta_do_servidor.grid(row = 1, column = 0, padx = 3, pady = 2)

    def criar_campo_da_porta_do_servidor(self):
        self.campo_da_porta_do_servidor = ttk.Entry(self.frame3)
        self.campo_da_porta_do_servidor.grid(row = 1, column = 1, padx = 3, pady = 2)

    def criar_botao_de_salvar(self):
        self.botao_de_salvar = ttk.Button(self.frame4, text = "Salvar", command = self.salvar_dados_de_configuracao)
        self.botao_de_salvar.grid(column = 0, columnspan = 2, pady = 2)

    def salvar_dados_de_configuracao(self):
        try:
            with open("json/config_cli.json", "w") as arquivo:
                dados_de_configuracao = {}
                dados_de_configuracao["ip_de_origem"] = self.campo_do_ip_de_origem.get().strip()
                dados_de_configuracao["ip_de_destino"] = self.campo_do_ip_de_destino.get().strip()
                dados_de_configuracao["porta_de_origem"] = int(self.campo_da_porta_de_origem.get().strip())
                dados_de_configuracao["porta_de_destino"] = int(self.campo_da_porta_de_destino.get().strip())
                dados_de_configuracao["ip_do_servidor"] = self.campo_do_ip_do_servidor.get().strip()
                dados_de_configuracao["porta_do_servidor"] = int(self.campo_da_porta_do_servidor.get().strip())

                json.dump(dados_de_configuracao, arquivo, indent = 4)

                MensagemDeSistema.criar_mensagem_de_sistema("info", "Sucesso!", "Configurações salvas com sucesso")

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Erro ao salvar dados", exception)

if __name__ == "__main__":
    ConfigCliGUI().janela.mainloop()