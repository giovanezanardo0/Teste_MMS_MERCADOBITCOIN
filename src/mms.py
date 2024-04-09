import json
import os
from datetime import datetime
from models import Moedas
from sqlalchemy.orm import sessionmaker
from database import engine


def get_valores_candle_moeda(arquivo_nome: str):
    # Obtendo o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Construindo o caminho absoluto para o arquivo JSON
    caminho_arquivo_json = os.path.join(diretorio_atual, arquivo_nome)

    # Lista para armazenar os valores de "close"
    valores_candle = []

    # Verificando se o arquivo existe
    if os.path.exists(caminho_arquivo_json):
        # Abrindo o arquivo JSON
        with open(caminho_arquivo_json, encoding="utf-8") as arquivo_mb:
            dados = json.load(arquivo_mb)

        # Iterando sobre os dados e armazenando os valores de "close"
        for item in dados["candles"]:
            valores_candle.append(
                {"close": item["close"], "timestamp": item["timestamp"]}
            )

    else:
        print(f"O arquivo '{arquivo_nome}' não foi encontrado.")

    return valores_candle


# Função para calcular a média móvel e inserir no banco de dados
def calcular_media_movel_e_inserir_no_banco(
    pair: str, valores_candle: dict, candle: dict
):
    media_movel_20d = 0
    media_movel_50d = 0
    media_movel_200d = 0
    count_20d = 1
    count_50d = 1
    count_200d = 1

    valores_candle_200 = []
    # pega os ultimos 20, 50 e 200 valores, anterior ao candle atual
    for valor in valores_candle:
        dias_de_diferenca = candle["timestamp"] - valor["timestamp"]

        # verifica se a diferença de dias é menor que 20, 50 e 200
        if int(dias_de_diferenca / 86400) < 200:
            valores_candle_200.append(valor)

        if valor["timestamp"] == candle["timestamp"]:
            break

    if not valores_candle_200:
        print(
            f"Não há dados suficientes para calcular a média móvel para o par {pair}."
        )
        return

    # invertendo a ordem dos valores para pegar a data decrescente
    valores_candle_200 = valores_candle_200[::-1]

    for valor in valores_candle_200:
        if count_20d <= 20:
            media_movel_20d += valor["close"]
        if count_50d <= 50:
            media_movel_50d += valor["close"]
        if count_200d <= 200:
            media_movel_200d += valor["close"]

        count_20d += 1
        count_50d += 1
        count_200d += 1

    media_movel_20d = media_movel_20d / min(count_20d, 20)
    media_movel_50d = media_movel_50d / min(count_50d, 50)
    media_movel_200d = media_movel_200d / min(count_200d, 200)

    print(f"Média Móvel Simples dos últimos 20 dias:", media_movel_20d)
    print(f"Média Móvel Simples dos últimos 50 dias:", media_movel_50d)
    print(f"Média Móvel Simples dos últimos 200 dias:", media_movel_200d)

    media_movel_obj = Moedas(
        pair=pair,
        timestamp=candle["timestamp"],
        mms_20d=media_movel_20d,
        mms_50d=media_movel_50d,
        mms_200d=media_movel_200d,
    )

    # Previne que sejam inseridos valores duplicados
    session = sessionmaker(bind=engine)()
    if (
        session.query(Moedas)
        .filter(Moedas.pair == pair, Moedas.timestamp == candle["timestamp"])
        .first()
    ):
        print(
            f"Os valores de médias móveis para o par {pair} e o timestamp {candle['timestamp']} já existem no banco de dados."
        )
        session.close()
        return

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(media_movel_obj)
    session.commit()


def load_data():
    valores_candle_btc = get_valores_candle_moeda("dados_api_mb_BTC.json")

    for candle in valores_candle_btc:
        calcular_media_movel_e_inserir_no_banco("BRLBTC", valores_candle_btc, candle)

    valores_candle_eth = get_valores_candle_moeda("dados_api_mb_ETH.json")
    for candle in valores_candle_eth:
        calcular_media_movel_e_inserir_no_banco("BRLETH", valores_candle_btc, candle)


load_data()
