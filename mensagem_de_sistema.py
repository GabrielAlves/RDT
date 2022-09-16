import tkinter as tk
from tkinter import messagebox as msg

class MensagemDeSistema:
    
    @classmethod
    def criar_mensagem_de_sistema(cls, tipo, titulo, conteudo):
        tipo = tipo.lower()

        if tipo == "info":
            msg.showinfo(titulo, conteudo)

        elif tipo == "warning":
            msg.showwarning(titulo, conteudo)

        elif tipo == "error":
            msg.showerror(titulo, conteudo)