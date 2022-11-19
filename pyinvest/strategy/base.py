from abc import ABC, abstractmethod
from typing import Type

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    order_time: Type[datetime]    # 委托时间
    filled_time: Type[datetime]   # 成交时间
    side: str                     # 交易方向
    total_amount: float           # 成交金额
    average_price: float          # 成交均价
    filled_amout: float           # 成交数量
    fee: float                    # 手续费


class Strategy(ABC):
    def __init__(self, *args, **kwargs):
        self._history = []
        self._cash = 0
        self._host = 0
        pass

    @property
    def cash(self):
        return self.cash

    @property
    def hold(self):
        return self._hold

    @abstractmethod
    def decide(self):
        pass

    @abstractmethod
    def update(self):
        pass
