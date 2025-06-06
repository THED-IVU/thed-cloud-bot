from datetime import datetime

class TradeManager:
    def __init__(self, capital, risk_per_trade=0.02, stop_loss_pips=10,
                 max_loss_day=3, max_win_chain=10, max_trades_per_day=10):
        self.capital = capital
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pips = stop_loss_pips
        self.max_loss_day = max_loss_day
        self.max_win_chain = max_win_chain
        self.max_trades_per_day = max_trades_per_day

        self.reset_day()
        self.last_reset_date = datetime.now().date()

    def compute_position_size(self, pip_value=10):
        perte_max = self.capital * self.risk_per_trade
        taille_lot = perte_max / (self.stop_loss_pips * pip_value)
        return round(taille_lot, 2)

    def on_trade_result(self, result):
        if result["statut"] != "ok":
            return

        self.trades_today += 1
        self.capital += result.get("profit", 0)

        if result["profit"] > 0:
            self.win_chain += 1
            self.losses_today = 0
        else:
            self.losses_today += 1
            self.win_chain = 0

        if self.losses_today >= self.max_loss_day:
            self.running = False
            print("🔴 STOP: Trop de pertes aujourd’hui.")

        if self.win_chain >= self.max_win_chain:
            self.running = False
            print("🟢 STOP: Séquence de gains maximale atteinte.")

        if self.trades_today >= self.max_trades_per_day:
            self.running = False
            print("⛔ STOP: Nombre de trades journaliers atteint.")

    def reset_day(self):
        self.trades_today = 0
        self.losses_today = 0
        self.win_chain = 0
        self.running = True

    def check_auto_reset(self):
        today = datetime.now().date()
        if today != self.last_reset_date:
            self.reset_day()
            self.last_reset_date = today

    def update_config(self, config: dict):
        self.risk_per_trade = config.get("risk_per_trade", self.risk_per_trade)
        self.stop_loss_pips = config.get("stop_loss_pips", self.stop_loss_pips)
        self.max_loss_day = config.get("max_loss_day", self.max_loss_day)
        self.max_win_chain = config.get("max_win_chain", self.max_win_chain)
        self.max_trades_per_day = config.get("max_trades_per_day", self.max_trades_per_day)

    def get_stats(self):
        return {
            "capital": round(self.capital, 2),
            "trades_today": self.trades_today,
            "losses_today": self.losses_today,
            "win_chain": self.win_chain,
            "running": self.running,
            "risk_per_trade": self.risk_per_trade,
            "stop_loss_pips": self.stop_loss_pips,
            "max_trades_per_day": self.max_trades_per_day
        }
