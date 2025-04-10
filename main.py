import random
from component import Component
from player import Player
from card import Card, Effect, Lifetime, Trigger
from enum import Enum, auto

class GameState(Enum):
    UNSTARTED = auto()
    PLAYER_TURN = auto()
    OPPONENT_TURN = auto()

# Define some effects
effect1: Effect = Effect()
effect2: Effect = Effect()

# Define some dummy cards and decks
card1: Card = Card()
card2: Card = Card()
card3: Card = Card()
card4: Card = Card()
card5: Card = Card()
card6: Card = Card()
card7: Card = Card()
card8: Card = Card()
card9: Card = Card()
card10: Card = Card()
card11: Card = Card()
card12: Card = Card()
card13: Card = Card()
card14: Card = Card()
card15: Card = Card()
card16: Card = Card()
card17: Card = Card()
card18: Card = Card()
card19: Card = Card()
card20: Card = Card()

playerDeck = [ card1, card2, card3, card4, card5, card6, card7, card8, card9, card10 ]
opponentDeck = [ card11, card12, card13, card14, card15, card16, card17, card18, card19, card20 ]

# Global State (ugly)
gameState: GameState = GameState.UNSTARTED
activeCards: list[Card] = []
player1 = Player("player", playerDeck)
player2 = Player("rando", opponentDeck)

def setup():
    print("Welcome to the game!")
    printInstructions()

def readInput():
    keyPress = input()
    return keyPress.lower()

def opponentPlay():
    rand_input = random.randint(1, 5)
    playedCard = playCard(rand_input, 2)
    return playedCard

def printInstructions():
    print('Type a command below then hit enter:')
    for i in range(len(player1.hand)):
        print(f"{i+1} -> Play card {i+1}")
    print('Q/q -> Quit the game')
    print(f"Player resources: {player1.resources}")
    print("Player hand:")
    for card in player1.hand:
        print(f"{card.name}")

def playCard(cardIdx: int, player: int):
    if player == 1:
        card = player1.playCard(cardIdx)
        activeCards.append(card)
    else:
        card = player2.playCard(cardIdx)
        activeCards.append(card)

def trigger(trigger: Trigger, component: Component):
    for card in activeCards:
        for effect in card.effects:
            if effect.trigger is trigger:
                effect.callback(component)

def checkLifetimes(lifetime: Lifetime):
    for card in activeCards:
        if card.lifetime is lifetime:
            activeCards.remove(card)
        

def run():
    setup()

    while True:
        checkLifetimes(Lifetime.NEXT_ROUND_START)
        printInstructions()
        key = readInput()

        if key == "q":
            break
        if int(key):
            playedCard = playCard(int(key), 1)
            return playedCard

    print("Bye bye")

if __name__ == "__main__":
    run()
