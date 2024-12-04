import time

class Bot:
    def __init__(self, api, estrategia):
        self.api = api
        self.estrategia = estrategia
        self.executando = False

    def iniciar(self, paridade):
        self.executando = True
        while self.executando:
            try:
                precos = self.api.obter_precos(paridade)
                sinal = self.estrategia.calcular_indicadores(precos)
                if sinal["sinal"]:
                    self.api.enviar_operacao(paridade, sinal["sinal"])
                time.sleep(60)  
            except Exception as e:
                print(f"Erro: {e}")
                self.executando = False
