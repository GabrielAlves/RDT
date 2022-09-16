import tkinter as tk
from tkinter import ttk
import json

from mensagem_de_sistema import MensagemDeSistema

class ConfigServGUI:
    def __init__(self):
        self.criar_widgets()
        self.mostrar_dados_de_configuracao()

    def mostrar_dados_de_configuracao(self):
        try:
            with open("json/config_serv.json", "r") as arquivo:
                dados_de_configuracao = json.load(arquivo) 
                self.preencher_campos(dados_de_configuracao)

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Erro ao ler arquivo de configurações", exception)

    def preencher_campos(self, dados_de_configuracao):
        ip = dados_de_configuracao["ip"]
        porta = dados_de_configuracao["porta"]

        self.inserir_texto_no_campo(self.campo_do_ip, ip)
        self.inserir_texto_no_campo(self.campo_da_porta, porta)

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

    def criar_frames(self):
        self.criar_frame1()
        self.criar_frame2()
        self.criar_frame3()
    
    def criar_frame1(self):
        self.frame1 = ttk.Frame(self.janela)
        self.frame1.pack(fill = tk.BOTH, expand = True)

    def criar_frame2(self):
        self.frame2 = ttk.Frame(self.janela)
        self.frame2.pack(fill = tk.BOTH, expand = True)

    def criar_frame3(self):
        self.frame3 = ttk.Frame(self.janela)
        self.frame3.pack(fill = tk.BOTH, expand = True)

    def criar_widgets_dos_frames(self):
        self.criar_widgets_do_frame1()
        self.criar_widgets_do_frame2()
        self.criar_widgets_do_frame3()

    def criar_widgets_do_frame1(self):
        self.criar_label_do_ip()
        self.criar_campo_do_ip()
        
    def criar_widgets_do_frame2(self):
        self.criar_label_da_porta()
        self.criar_campo_da_porta()

    def criar_widgets_do_frame3(self):
        self.criar_botao_de_salvar()

    def criar_label_do_ip(self):
        self.label_do_ip = ttk.Label(self.frame1, text = "IP", font = ("Arial", 12))
        self.label_do_ip.grid(row = 0, column = 0, padx = 3, pady = 2)  

    def criar_campo_do_ip(self):
        self.campo_do_ip = ttk.Entry(self.frame1)
        self.campo_do_ip.grid(row = 0, column = 1, padx = 3, pady = 2, sticky = tk.NSEW)
        self.campo_do_ip.focus()

    def criar_label_da_porta(self):
        self.label_da_porta = ttk.Label(self.frame2, text = "Porta", font = ("Arial", 12))
        self.label_da_porta.grid(row = 0, column = 0, padx = 3, pady = 2)

    def criar_campo_da_porta(self):
        self.campo_da_porta = ttk.Entry(self.frame2)
        self.campo_da_porta.grid(row = 0, column = 1, padx = 3, pady = 2)

    def criar_botao_de_salvar(self):
        self.botao_de_salvar = ttk.Button(self.frame3, text = "Salvar", command = self.salvar_dados_de_configuracao)
        self.botao_de_salvar.grid(column = 0, columnspan = 2, pady = 2)

    def salvar_dados_de_configuracao(self):
        try:
            with open("json/config_serv.json", "w") as arquivo:
                dados_de_configuracao = {}
                dados_de_configuracao["ip"] = self.campo_do_ip.get().strip()
                dados_de_configuracao["porta"] = int(self.campo_da_porta.get().strip())

                json.dump(dados_de_configuracao, arquivo, indent = 4)

                MensagemDeSistema.criar_mensagem_de_sistema("info", "Sucesso!", "Configurações salvas com sucesso")

        except Exception as exception:
            MensagemDeSistema.criar_mensagem_de_sistema("error", "Erro ao salvar dados", exception)

if __name__ == "__main__":
    ConfigServGUI().janela.mainloop()