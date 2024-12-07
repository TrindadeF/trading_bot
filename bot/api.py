import requests

class DruOptionAPI:
    def __init__(self):
        self.base_url = "https://platform-api.us-a.tradesmarter.com"
        self.session = None
        self.user_id = None

    def get_session(self, user_id):
        """
        Obtém a sessão para o usuário.
        """
        url = f"{self.base_url}/index/get-session"
        params = {"userID": user_id}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            result = response.json()
            self.session = result["session"]
            return self.session

        raise Exception(f"Erro ao obter sessão: {response.status_code}, {response.text}")

    def get_options(self, assets="1,139", game_type=2):
        """
        Obtém a lista de opções disponíveis.
        """
        url = f"{self.base_url}/index/get-options"
        params = {
            "assets": assets,
            "gameType": game_type
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

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
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Erro ao executar trade: {response.status_code}, {response.text}")

# Exemplo de uso
if __name__ == "__main__":
    api = SimpleTraderAPI()

    try:
        user_id = 761415  # Substitua pelo seu userID real
        session = api.get_session(user_id)
        print(f"Sessão obtida: {session}")

        options = api.get_options()
        print(f"Opções disponíveis: {options}")

        # Para executar uma trade (substitua com valores reais)
        trade_response = api.trade_option(option_id="879f1a7a96a02962", direction=1, stake=5)
        print(f"Trade executada: {trade_response}")

    except Exception as e:
        print(f"Erro: {str(e)}")
