from component import Component
from card import Card
from event_handling import EventDispatcher
import random

class Player(Component):
    def __init__(self, name, deck: list[Card]):
        super().__init__(name)
        self.hand: list[Card] = []
        self.deck: list[Card] = deck
        self.resources = 100
        self.score = 0
        self.game_board = Component("board")
        self.dispatcher = EventDispatcher()
        for _ in range(5):
            self.hand.append(self.drawCard())

    def playCard(self, idx: int):
        card = self.hand[idx-1]
        self.resources -= card.cost
        self.hand.remove(card)
        return card

    def drawCard(self) -> Card:
        rand_draw = random.randint(0, len(self.deck)-1)
        card = self.deck[rand_draw]
        self.deck.remove(card)
        return card
