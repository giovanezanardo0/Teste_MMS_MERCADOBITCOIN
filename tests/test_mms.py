from mms import get_valores_candle_moeda


def test_get_candles_btc():
    valores = get_valores_candle_moeda("dados_api_mb_BTC.json")
    assert valores != None


def test_get_candles_eth():
    valores = get_valores_candle_moeda("dados_api_mb_ETH.json")
    assert valores != None
