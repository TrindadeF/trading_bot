from bot.api import DruOptionAPI


class Bot:
    def __init__(self, api, estrategia):
        self.api = api
        self.estrategia = estrategia
        self.user_id = None
        self.session = None
        self.executando = False

    def login(self, email, password):
        print("Realizando login...")
        login_data = self.api.login(email, password)
        self.user_id = login_data["userID"]
        self.session = login_data["session"]
        print(f"Login realizado com sucesso! User ID: {self.user_id}")

    def iniciar(self, assets="1,139", stake=10):
        if not self.session:
            raise Exception("Sessão inválida. Realize o login antes de iniciar o robô.")

        print("Iniciando o robô...")
        self.executando = True

        while self.executando:
            try:
                opcoes = self.api.listar_opcoes(assets=assets)
                precos = [op["price"] for op in opcoes["options"]]

                sinal = self.estrategia.calcular_indicadores(precos)

                if sinal["sinal"] and sinal["preco"]:
                    direction = "up" if sinal["sinal"] == "call" else "down"
                    option_id = opcoes["options"][0]["optionID"] 

                    print(f"Executando trade - Direction: {direction}, Stake: {stake}")
                    resultado = self.api.executar_trade(option_id, direction, stake)
                    print(f"Resultado do trade: {resultado}")

            except Exception as e:
                print(f"Erro durante execução: {e}")
                self.parar()

    def parar(self):
        """
        Interrompe o robô.
        """
        print("Parando o robô...")
        self.executando = False
