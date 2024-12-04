import tkinter as tk
from tkinter import messagebox
from bot.api import DruOptionAPI
from bot.bot import Bot
from bot.strategy import Estrategia


class App:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("DruOption Bot")
        self.janela.geometry("400x500")
        self.janela.configure(bg="#000000")  
        self.api = None
        self.bot = None

        self.criar_tela_login()

    def criar_tela_login(self):
        header_frame = tk.Frame(self.janela, bg="#000000")
        header_frame.pack(pady=30)

        tk.Label(header_frame, text="DruOption Bot", font=("Arial", 20, "bold"), bg="#000000", fg="#00FF00").pack()
        tk.Label(header_frame, text="Faça login para começar", font=("Arial", 12), bg="#000000", fg="#00FF00").pack()

        form_frame = tk.Frame(self.janela, bg="#0d4d00", padx=20, pady=20)  
        form_frame.pack(pady=20, fill="x", expand=True)

        tk.Label(form_frame, text="Usuário", font=("Arial", 12), bg="#0d4d00", fg="#00FF00").pack(anchor="w", pady=(10, 0))
        self.usuario_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.usuario_entry.pack(fill="x", pady=(0, 10))

        tk.Label(form_frame, text="Senha", font=("Arial", 12), bg="#0d4d00", fg="#00FF00").pack(anchor="w", pady=(10, 0))
        self.senha_entry = tk.Entry(form_frame, font=("Arial", 12), show="*")
        self.senha_entry.pack(fill="x", pady=(0, 20))

        tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=self.realizar_login).pack(fill="x", pady=10)

    def criar_dashboard(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        tk.Label(self.janela, text="Painel de Controle", font=("Arial", 20, "bold"), bg="#000000", fg="#00FF00").pack(pady=20)

        saldo = self.api.obter_saldo()
        tk.Label(self.janela, text=f"Saldo: {saldo:.2f}", font=("Arial", 14), bg="#000000", fg="#00FF00").pack(pady=10)

        tk.Button(self.janela, text="Iniciar Bot", font=("Arial", 12, "bold"), bg="#0d4d00", fg="#00FF00", command=self.iniciar_bot).pack(pady=10)
        tk.Button(self.janela, text="Parar Bot", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=self.parar_bot).pack(pady=10)

    def realizar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        try:
            self.api = DruOptionAPI(api_key="api_key_aqui")
            self.api.login(usuario, senha)
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.criar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro de Login", f"Erro: {e}")

    def iniciar_bot(self):
        estrategia = Estrategia()
        self.bot = Bot(api=self.api, estrategia=estrategia)
        self.bot.iniciar(paridade="EUR/USD")

    def parar_bot(self):
        if self.bot:
            self.bot.executando = False
            messagebox.showinfo("Bot", "Bot parado com sucesso!")

    def executar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = App()
    app.executar()
