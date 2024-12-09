import requests
from requests.auth import HTTPBasicAuth

class DruOptionAPI:
    def __init__(self, username, password):
        self.base_url = "https://platform-api.us-a.tradesmarter.com"
        self.auth = HTTPBasicAuth(username, password)  # Configura autenticação básica
        self.session = None  # Sessão do usuário (obtida no login)

    def get_session(self, user_id):
        """
        Obtém a sessão para o usuário baseado no `userID` informado.
        """
        url = f"{self.base_url}/index/get-session"
        params = {"userID": user_id}

        response = requests.get(url, params=params, auth=self.auth, timeout=30)  # Adiciona timeout

        if response.status_code == 200:
            result = response.json()
            self.session = result.get("session")
            if self.session:
                return self.session
            else:
                raise Exception("Sessão não encontrada na resposta.")
        else:
            raise Exception(f"Erro ao obter sessão: {response.status_code}, {response.text}")

    def get_options(self, assets="1,139", game_type=2):
        """
        Obtém a lista de opções disponíveis.
        """
        if not self.session:
            raise Exception("Sessão não encontrada. Realize o login primeiro.")

        url = f"{self.base_url}/index/get-options"
        params = {
            "assets": assets,
            "gameType": game_type,
            "session": self.session  # Inclui sessão nos parâmetros
        }

        response = requests.get(url, params=params, auth=self.auth, timeout=30)  # Adiciona timeout

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao listar opções: {response.status_code}, {response.text}")

    def trade_option(self, option_id, direction, stake):
        """
        Executa uma trade para o usuário com a sessão ativa.
        """
        if not self.session:
            raise Exception("Sessão não encontrada. Realize o login primeiro.")

        url = f"{self.base_url}/user/trade-option"
        params = {
            "session": self.session,
            "option": option_id,
            "direction": direction,
            "stake": stake
        }

        response = requests.get(url, params=params, auth=self.auth, timeout=30)  # Adiciona timeout

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao executar trade: {response.status_code}, {response.text}")
