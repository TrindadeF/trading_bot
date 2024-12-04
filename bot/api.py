import requests

class DruOptionAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://api.druoption.com/v1"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def login(self, username: str, password: str):
        url = f"{self.base_url}/auth/login"
        payload = {"username": username, "password": password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  
        raise Exception("Erro no login: " + response.text)

    def obter_saldo(self):
        url = f"{self.base_url}/account/saldo"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["saldo"]
        raise Exception("Erro ao obter saldo: " + response.text)

    def enviar_operacao(self, paridade: str, tipo: str):
        url = f"{self.base_url}/operacoes"
        payload = {"paridade": paridade, "tipo": tipo}
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception("Erro ao enviar operação: " + response.text)

    def obter_precos(self, paridade: str):
        url = f"{self.base_url}/precos/{paridade}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["precos"]
        raise Exception("Erro ao obter preços: " + response.text)
