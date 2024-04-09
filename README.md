# Websocket

## Python

Check python version.

This examples requires python 3.9.10

```
$ python --version
Python 3.9.10
```

## Install dependencies

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
