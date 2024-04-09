from fastapi import FastAPI, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from models import Moedas
from typing import List, Optional
from database import get_db
from datetime import datetime, timedelta

app = FastAPI()


# Endpoint para exibir valores de médias móveis para um par e um intervalo de tempo específicos
# Exemplo: http://127.0.0.1:8000/BRLBTC/mms/?from=1680535828&to=1711756800&range=200
# API USADA MB https://mobile.mercadobitcoin.com.br/v4/BRLETH/candle?from=1641051000&to=1711812600&precision=1d
@app.get("/{pair}/mms/")
def exibir_valores_moedas_por_par_e_range(
    request: Request,
    pair: str,
    from_timestamp: Optional[int] = Query(None, alias="from"),
    to_timestamp: Optional[int] = Query(None, alias="to"),
    range_value: Optional[int] = Query(None, alias="range"),
    db: Session = Depends(get_db),
):
    # Verifica se o par de moedas é válido
    if pair not in ["BRLBTC", "BRLETH"]:  # Adicione outros pares conforme necessário
        raise HTTPException(
            status_code=400, detail=f"Par de moeda {pair} não é suportado"
        )
    # Verifica se o range é válido
    if range_value not in [20, 50, 200]:
        raise HTTPException(
            status_code=400, detail=f"O valor de range {range_value} não é suportado"
        )
    # Data atual e Data Limite
    data_atual = datetime.now()
    # Verifica se a data inicial está dentro do limite de 365 dias em relação à data atual
    data_limite = data_atual - timedelta(days=365)
    # Convertendo a data para timestamp inteiro
    timestamp_limite = int(data_limite.timestamp())
    # Verifica se a data inicial é anterior a 365 e exibe uma mensagem de aviso
    if from_timestamp < timestamp_limite:
        raise HTTPException(
            status_code=400, detail="A data de início não pode ser anterior a 365 dias"
        )
    # Busca os valores de médias móveis para o par de moedas e o intervalo de tempo especificado
    valores_moedas = (
        db.query(Moedas)
        .filter(
            Moedas.pair == pair,
            Moedas.timestamp >= from_timestamp,
            Moedas.timestamp <= to_timestamp,
        )
        .all()
    )
    # Verifica se foram encontrados valores para o par e o intervalo de tempo especificados
    if not valores_moedas:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum valor de moeda encontrado para o par {pair} e o intervalo de tempo especificado",
        )
    # Mapeia o valor de range para o nome do atributo correspondente
    if range_value == 20:
        mms_attr = "mms_20d"
    elif range_value == 50:
        mms_attr = "mms_50d"
    elif range_value == 200:
        mms_attr = "mms_200d"
    # Constrói a resposta com os valores de médias móveis
    mms_retorno = []
    for valor in valores_moedas:
        mms_retorno.append(
            {"timestamp": valor.timestamp, "mms": getattr(valor, mms_attr)}
        )
    return mms_retorno
