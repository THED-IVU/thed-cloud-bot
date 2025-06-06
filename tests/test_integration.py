import pytest
import pandas as pd
from datetime import datetime

from trading import enregistrer_trade, lire_trades
from scanner import scanner_actifs
from ai import analyser_avec_ia


def test_scanner_actifs():
    df = scanner_actifs()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_trade_enregistrement_et_lecture():
    fake_trade = {
        "datetime": datetime.now().isoformat(),
        "action": "BUY",
        "price": 1.1234,
        "exit_price": 1.1244,
        "profit": 0.0010,
        "RSI": 50,
        "MACD": 0.002,
        "MACDs": 0.001,
        "EMA9": 1.12,
        "EMA21": 1.13,
        "source": "TEST",
        "context": "uptrend",
        "note": 7.5,
        "asset": "TESTUSD"
    }
    enregistrer_trade(fake_trade)
    df = lire_trades()
    assert "asset" in df.columns
    assert "profit" in df.columns
    assert df[df["asset"] == "TESTUSD"].shape[0] > 0


def test_analyse_ia_format():
    sample_df = pd.DataFrame({
        "close": [1.1, 1.11, 1.12, 1.13, 1.14],
        "rsi": [45, 46, 47, 48, 49],
        "macd_12_26_9": [0.001]*5,
        "macds_12_26_9": [0.0005]*5,
        "ema9": [1.1]*5,
        "ema21": [1.11]*5,
        "signal": ["HOLD"]*5
    })
    result = analyser_avec_ia(sample_df)
    assert isinstance(result, dict)
    assert "ACTION" in result
    assert "SCORE" in result
