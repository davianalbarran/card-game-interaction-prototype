from enum import Enum, auto
from typing import Callable
from component import Component

class Lifetime(Enum):
    INDEFINITE = auto()
    ROUND_END = auto()
    NEXT_ROUND_START = auto()
    PLAYER_TURN_END = auto()
    OPPONENT_TURN_END = auto()

class Target(Enum):
    SELF_GAME_BOARD = auto()
    OPPONENT_GAME_BOARD = auto()
    SELF = auto()
    OPPONENT = auto()

class Trigger(Enum):
    ON_PLAY = auto()
    ON_DESTROY = auto()
    ON_OPPONENT_HIT = auto()
    ON_SELF_HIT = auto()

class Effect:
    def __init__(self, target: Target, trigger: Trigger, onTrigger: Callable[[Component], None]):
        self.target = target
        self.trigger = trigger
        self.onTrigger = onTrigger

class Card(Component):
    def __init__(self, name: str, cost: int, effects: list[Effect], lifetime = Lifetime.INDEFINITE):
        super().__init__(name)
        self.cost = cost
        self.effects = effects
        self.lifetime = lifetime

    def display(self):
        print(self.name)
