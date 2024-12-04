import pandas as pd
import pandas_ta as ta

class Estrategia:
    def __init__(self):
        pass

    def calcular_indicadores(self, precos):
        df = pd.DataFrame(precos, columns=["close"])
        df["RSI"] = ta.rsi(df["close"], length=14)

        bb = ta.bbands(df["close"], length=20, std=2)
        df = pd.concat([df, bb], axis=1)

        ultimo_preco = df["close"].iloc[-1]
        ultimo_rsi = df["RSI"].iloc[-1]
        banda_superior = df["BBU_20_2.0"].iloc[-1]
        banda_inferior = df["BBL_20_2.0"].iloc[-1]

        if ultimo_preco <= banda_inferior and ultimo_rsi <= 30:
            return {"sinal": "call", "preco": ultimo_preco}
        elif ultimo_preco >= banda_superior and ultimo_rsi >= 70:
            return {"sinal": "put", "preco": ultimo_preco}
        else:
            return {"sinal": None, "preco": ultimo_preco}
