## Python

Verifique a versão do python.

Este exemplo requer python 3.9.10

```
$ python --version
Python 3.9.10
```

## Instalar dependências

```
$ pip install -r requirements.txt
```

## Run

```1 instalar dependencias
    make requirements
```

```2 carregar arquivos iniciais no banco local
    make load-data
```

```3 Rodar o servidor
    make run
```

## Acessando o Docs

```
    http://127.0.0.1:8000/docs
```

## Exemplo de chamadas:

### Exemplo de chamada para o endpoint de média móvel simples BTC 20 dias

```
http://127.0.0.1:8000/BRLBTC/mms/?from=1708732800&to=1709251200&range=20
```

### Exemplo de chamada para o endpoint de média móvel simples ETH 200 dias

```
http://127.0.0.1:8000/BRLETH/mms/?from=1703289600&to=1703635200&range=200
```


### Exemplo de chamada com erro, pois maior que 365 dias

```
http://127.0.0.1:8000/BRLBTC/mms/?from=1680535828&to=1711756800&range=50
```

Observação:

Na estrutura, adicionei dois arquivos contendo os dados das moedas em formato JSON, abrangendo um período de 2 anos (de 01/01/2022, 21:00:00 até 29/03/2024, 21:00:00). Esses arquivos, chamados dados_api_mb_BTC.json e dados_api_mb_ETH.json, desempenhariam o papel da API do Mercado Bitcoin. Ao tentar criar uma lógica para buscar os dados diretamente da API, me deparei com um erro 403, impedindo o acesso às informações necessárias. Essa solução alternativa foi pensada como uma maneira de prosseguir com o teste.
