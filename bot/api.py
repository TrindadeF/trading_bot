import requests


class DruOptionAPI:
    def __init__(self):
        self.base_url = "https://platform-api.us-a.tradesmarter.com"
        self.session = None 
        self.user_id = None  

    def login(self, email, password):
        url = f"{self.base_url}/user/login"
        data = {"email": email, "password": password}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            result = response.json()
            self.user_id = result["userID"]
            self.session = result["session"]
            return result

        raise Exception(f"Erro ao fazer login: {response.text}")

    def listar_opcoes(self, assets="1,139", game_type=2):
        if not self.session:
            raise Exception("Sessão inválida. Realize o login primeiro.")

        url = f"{self.base_url}/index/get-options"
        params = {
            "assets": assets,
            "gameType": game_type,
            "session": self.session
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Erro ao listar opções: {response.text}")

    def criar_sessao(self):
        if not self.user_id:
            raise Exception("User ID não encontrado. Realize o login primeiro.")

        url = f"{self.base_url}/index/get-session"
        params = {"userID": self.user_id}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            self.session = response.json()["session"]
            return self.session

        raise Exception(f"Erro ao criar sessão: {response.text}")

    def executar_trade(self, option_id, direction, stake):
        if not self.session:
            raise Exception("Sessão inválida. Realize o login primeiro.")

        url = f"{self.base_url}/user/trade-option"
        params = {
            "session": self.session,
            "option": option_id,
            "direction": direction,
            "stake": stake,
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Erro ao executar trade: {response.text}")

    def obter_saldo(self):
        if not self.session:
            raise Exception("Sessão inválida. Realize o login primeiro.")

        url = f"{self.base_url}/user/get-balance"
        params = {"session": self.session}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json().get("balance", 0.0)

        raise Exception(f"Erro ao obter saldo: {response.text}")
