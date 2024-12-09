import os
import tkinter as tk
from tkinter import messagebox, Toplevel
from threading import Thread
from dotenv import load_dotenv
from bot.api import DruOptionAPI

load_dotenv()

class App:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("DruOption Bot")
        self.janela.geometry("400x600")
        self.janela.configure(bg="#000000")
        self.api = None

        self.username = os.getenv("DRUOPTION_API_USERNAME")
        self.password = os.getenv("DRUOPTION_API_PASSWORD")

        if not self.username or not self.password:
            messagebox.showerror("Erro", "As variáveis de ambiente para username e password não foram configuradas.")
            self.janela.destroy()
            return

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

        tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=self.iniciar_login_thread).pack(fill="x", pady=10)

    def iniciar_login_thread(self):
        """
        Inicia o login em uma thread separada.
        """
        user_id = self.usuario_entry.get()

        if not user_id.isdigit():
            messagebox.showerror("Erro de Login", "O ID do usuário deve conter apenas números.")
            return

        thread = Thread(target=self.realizar_login, args=(user_id,))
        thread.start()

    def realizar_login(self, user_id):
        """
        Realiza o login utilizando uma thread separada.
        """
        try:
            self.api = DruOptionAPI(username=self.username, password=self.password)
            session = self.api.get_session(user_id)

            # Atualiza a interface na thread principal
            self.janela.after(0, lambda: self.login_sucesso())
        except Exception as e:
            # Exibe o erro na thread principal
            self.janela.after(0, lambda: messagebox.showerror("Erro de Login", f"Erro ao tentar fazer login: {e}"))

    def login_sucesso(self):
        """
        Chamada após o login bem-sucedido.
        """
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        self.criar_dashboard()

    def criar_dashboard(self):
        """
        Cria o painel de controle após o login.
        """
        for widget in self.janela.winfo_children():
            widget.destroy()

        tk.Label(self.janela, text="Painel de Controle", font=("Arial", 20, "bold"), bg="#000000", fg="#00FF00").pack(pady=20)

        self.saldo_label = tk.Label(self.janela, text="Saldo: Carregando...", font=("Arial", 14), bg="#000000", fg="#00FF00")
        self.saldo_label.pack(pady=10)

        tk.Button(self.janela, text="Listar Opções", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=self.listar_opcoes).pack(pady=10)
        tk.Button(self.janela, text="Executar Trade", font=("Arial", 12, "bold"), bg="#0d4d00", fg="#00FF00", command=self.criar_tela_trade).pack(pady=10)
        tk.Button(self.janela, text="Sair", font=("Arial", 12, "bold"), bg="#FF0000", fg="#FFFFFF", command=self.janela.quit).pack(pady=10)

    def listar_opcoes(self):
        try:
            options = self.api.get_options(assets="1,139", game_type=2)
            options_window = Toplevel(self.janela)
            options_window.title("Opções Disponíveis")
            options_window.geometry("600x400")
            options_window.configure(bg="#000000")

            tk.Label(options_window, text="Opções Disponíveis", font=("Arial", 16, "bold"), bg="#000000", fg="#00FF00").pack(pady=10)

            for option in options:
                option_text = f"OptionID: {option['optionID']} | Asset: {option['assetName']} | EndTime: {option['endTime']}"
                tk.Label(options_window, text=option_text, font=("Arial", 12), bg="#000000", fg="#00FF00").pack(anchor="w")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar opções: {e}")

    def criar_tela_trade(self):
        trade_window = Toplevel(self.janela)
        trade_window.title("Executar Trade")
        trade_window.geometry("400x300")
        trade_window.configure(bg="#000000")

        tk.Label(trade_window, text="Executar Trade", font=("Arial", 16, "bold"), bg="#000000", fg="#00FF00").pack(pady=10)

        tk.Label(trade_window, text="Option ID:", font=("Arial", 12), bg="#000000", fg="#00FF00").pack(anchor="w", pady=(10, 0))
        option_id_entry = tk.Entry(trade_window, font=("Arial", 12))
        option_id_entry.pack(fill="x", pady=(0, 10))

        tk.Label(trade_window, text="Direção (1 para call, -1 para put):", font=("Arial", 12), bg="#000000", fg="#00FF00").pack(anchor="w", pady=(10, 0))
        direction_entry = tk.Entry(trade_window, font=("Arial", 12))
        direction_entry.pack(fill="x", pady=(0, 10))

        tk.Label(trade_window, text="Valor do Investimento:", font=("Arial", 12), bg="#000000", fg="#00FF00").pack(anchor="w", pady=(10, 0))
        stake_entry = tk.Entry(trade_window, font=("Arial", 12))
        stake_entry.pack(fill="x", pady=(0, 10))

        def executar_trade():
            option_id = option_id_entry.get()
            direction = direction_entry.get()
            stake = stake_entry.get()

            if not option_id or not direction or not stake:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            try:
                trade_response = self.api.trade_option(option_id, int(direction), float(stake))
                messagebox.showinfo("Trade", f"Trade realizado com sucesso! ID: {trade_response['tradeID']}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao executar trade: {e}")

        tk.Button(trade_window, text="Executar Trade", font=("Arial", 12, "bold"), bg="#00FF00", fg="#000000", command=executar_trade).pack(pady=20)

    def executar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = App()
    app.executar()
