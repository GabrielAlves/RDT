import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class ClienteGUI:
    def __init__(self):
        self.criar_widgets()

    def criar_widgets(self):
        self.criar_janela()
        self.criar_frames()
        self.criar_widgets_do_frame2()

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
        self.criar_frame4()

    def criar_frame1(self):
        self.frame1 = tk.Frame(self.janela)
        self.frame1.pack()

    def criar_frame2(self):
        self.frame2 = ttk.Frame(self.janela)
        self.frame2.pack(fill = tk.BOTH, expand = False, side = tk.BOTTOM)

    def criar_frame3(self):
        self.frame3 = ttk.Frame(self.frame2)
        self.frame3.grid(row = 0, column = 0, padx = 1, pady = 1)
        # self.frame3.grid_columnconfigure(0, weight = 1)

    def criar_frame4(self):
        self.frame4 = ttk.Frame(self.frame2)
        self.frame4.grid(row = 0, column = 1, padx = 1, pady = 1)
        # self.frame3.grid_columnconfigure(0, weight = 1)

    def criar_widgets_do_frame2(self):
        self.criar_caixa_de_texto()
        self.criar_botao_de_anexar_imagem()
        self.criar_botao_de_enviar()

    def criar_caixa_de_texto(self):
        self.caixa_de_texto = scrolledtext.ScrolledText(self.frame3, width = 33, height = 1, font = ("Arial", 12), wrap = tk.WORD)
        self.caixa_de_texto.grid()
        self.caixa_de_texto.focus()

    def criar_botao_de_anexar_imagem(self):
        self.botao_de_anexar_imagem = ttk.Button(self.frame4, text = "Anexar")
        self.botao_de_anexar_imagem.grid(row = 0)

    def criar_botao_de_enviar(self):
        self.botao_de_anexar_imagem = ttk.Button(self.frame4, text = "Enviar")
        self.botao_de_anexar_imagem.grid(row = 1)

if __name__ == "__main__":
    ClienteGUI().janela.mainloop()