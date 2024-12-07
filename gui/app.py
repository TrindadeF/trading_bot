import tkinter as tk
from tkinter import messagebox
from bot.api import DruOptionAPI
from bot.bot import Bot
from bot.strategy import Estrategia

class App:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("DruOption Bot")
        self.janela.geometry("400x600")
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

        tk.Label(form_frame, text="ID do Usuário", font=("Arial", 12), bg="#0d4d00", fg="#00FF00").pack(anchor="w", pady=(10, 0))
        self.usuario_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.usuario_entry.pack(fill="x", pady=(0, 10))

        tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=self.realizar_login).pack(fill="x", pady=10)

    def criar_dashboard(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        tk.Label(self.janela, text="Painel de Controle", font=("Arial", 20, "bold"), bg="#000000", fg="#00FF00").pack(pady=20)

        self.saldo_label = tk.Label(self.janela, text="Saldo: Carregando...", font=("Arial", 14), bg="#000000", fg="#00FF00")
        self.saldo_label.pack(pady=10)
        self.atualizar_saldo()

        tk.Label(self.janela, text="Paridade:", font=("Arial", 12), bg="#000000", fg="#00FF00").pack(pady=(20, 5))
        self.paridade_var = tk.StringVar(value="EUR/USD")
        paridades = ["EUR/USD", "USD/JPY", "GBP/USD"]
        self.paridade_menu = tk.OptionMenu(self.janela, self.paridade_var, *paridades)
        self.paridade_menu.configure(font=("Arial", 12), bg="#0d4d00", fg="#00FF00")
        self.paridade_menu.pack()

        tk.Button(self.janela, text="Atualizar Saldo", font=("Arial", 12, "bold"), bg="#0d4d00", fg="#00FF00", command=self.atualizar_saldo).pack(pady=10)
        tk.Button(self.janela, text="Iniciar Bot", font=("Arial", 12, "bold"), bg="#0d4d00", fg="#00FF00", command=self.iniciar_bot).pack(pady=10)
        tk.Button(self.janela, text="Parar Bot", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=self.parar_bot).pack(pady=10)

    def realizar_login(self):
        user_id = self.usuario_entry.get()  # Agora, espera-se o ID do usuário, não o nome ou senha

        if not user_id:
            messagebox.showerror("Erro de Login", "Por favor, preencha o ID do usuário.")
            return

        try:
            self.api = DruOptionAPI()
            self.api.get_session(user_id)  # Usando o ID do usuário para obter a sessão
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.criar_dashboard()
        except Exception as e:
            messagebox.showerror("Erro de Login", f"Erro ao tentar fazer login: {e}")

    def atualizar_saldo(self):
        try:
            saldo = self.api.get_options()  # Supondo que a API forneça um método de saldo
            self.saldo_label.config(text=f"Saldo: {saldo['balance']:.2f}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter saldo: {e}")

    def iniciar_bot(self):
        paridade = self.paridade_var.get()
        if not self.bot:
            estrategia = Estrategia()
            self.bot = Bot(api=self.api, estrategia=estrategia)

        if not self.bot.executando:
            try:
                self.bot.iniciar(paridade=paridade)
                messagebox.showinfo("Bot", "Bot iniciado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao iniciar o bot: {e}")
        else:
            messagebox.showinfo("Bot", "Bot já está em execução.")

    def parar_bot(self):
        if self.bot and self.bot.executando:
            self.bot.executando = False
            messagebox.showinfo("Bot", "Bot parado com sucesso!")
        else:
            messagebox.showinfo("Bot", "Bot não está em execução.")

    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = App()
    app.executar()
