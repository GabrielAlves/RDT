import textwrap
import tkinter as tk

class MensagemDeUsuario:
    def __init__(self, janela, canvas):
        self.espacamento_entre_mensagens = 0
        self.eh_a_primeira_mensagem = True
        self.janela = janela
        self.canvas = canvas
        
    def criar_balao_de_mensagem(self, texto_da_mensagem, eh_local):
        if self.eh_a_primeira_mensagem:
            self.eh_a_primeira_mensagem = False
        
        else:
            self.canvas.move(tk.ALL, 0, -self.espacamento_entre_mensagens - 15)

        mensagem_formatada = textwrap.fill(texto_da_mensagem, 20)
        
        frame_da_mensagem = tk.Frame(self.canvas, bg = "light grey")
        xinicial_da_mensagem = 85 if eh_local else 310
        frame_auxiliar = self.canvas.create_window(xinicial_da_mensagem, 260, window = frame_da_mensagem)
        tk.Label(frame_da_mensagem, text = mensagem_formatada, font=("Helvetica", 9), bg="light grey").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.janela.update_idletasks()
        pontos_do_triangulo = self.definir_triangulo_da_mensagem(frame_auxiliar, eh_local)
        self.canvas.create_polygon(pontos_do_triangulo, fill="light grey", outline="light grey")

    def definir_triangulo_da_mensagem(self, frame_auxiliar, eh_local):
        x1, y1, x2, y2 = self.canvas.bbox(frame_auxiliar)

        self.espacamento_entre_mensagens = y2 - y1

        if eh_local:
            return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2

        else:
            return x2, y2, x2, y2 - 10, x2 + 15, y2 + 10 