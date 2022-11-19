from pyinvest.strategy import Strategy

class Gridbase(Strategy):
    def __init__(
        self, lower_price, upper_price, grid_quantity, invest_amount, take_profit_price, stop_loss_price, grid_mode='arithmetic'
    ):
        super().__init__()
        # Price range: [Lower, Upper]
        # Grid mode: {Arithmetic, Geometric} and quantity int:
        # Investment amount
        # Take Profit/Stop Loss
    
    def decide(self):
        pass

    def update(self):
        pass