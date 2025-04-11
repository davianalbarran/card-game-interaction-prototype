import random
from component import Component
from player import Player
from card import Card, Effect, Lifetime, Target, Trigger
from enum import Enum, auto
from effects import freezePlayer, unfreezePlayer

class GameState(Enum):
    UNSTARTED = auto()
    PLAYER_TURN = auto()
    OPPONENT_TURN = auto()

# Define some effects
freezeOpponentEffect: Effect = Effect(Target.OPPONENT, Trigger.ON_PLAY, freezePlayer)
unfreezeOpponentEffect: Effect = Effect(Target.OPPONENT, Trigger.ON_DESTROY, unfreezePlayer)

# Define some dummy cards and decks
card1: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card2: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card3: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card4: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card5: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card6: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card7: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card8: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card9: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card10: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card11: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card12: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card13: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card14: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card15: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card16: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card17: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card18: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card19: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)
card20: Card = Card("Freeze opponent", 3, [freezeOpponentEffect, unfreezeOpponentEffect], Lifetime.ROUND_END)

playerDeck = [ card1, card2, card3, card4, card5, card6, card7, card8, card9, card10 ]
opponentDeck = [ card11, card12, card13, card14, card15, card16, card17, card18, card19, card20 ]

# Global State (ugly)
gameState: GameState = GameState.UNSTARTED
activeCards: list[Card] = []
player_self = Player("player", playerDeck)
opponent = Player("rando", opponentDeck)

def setup():
    print("Welcome to the game!")

def readInput():
    keyPress = input()
    return keyPress.lower()

def opponentPlay():
    rand_input = random.randint(1, len(opponent.hand))
    playedCard = playCard(rand_input, 2)
    return playedCard

def printInstructions():
    print('Type a command below then hit enter:')
    for i in range(len(player_self.hand)):
        print(f"{i+1} -> Play card {i+1}")
    print('Q/q -> Quit the game\n')
    print(f"Player resources: {player_self.resources}")
    print("Player hand:")
    index = 1
    for card in player_self.hand:
        print(f"{index} - {card.name}")
        index += 1

def activateCard(card: Card):
    for effect in card.effects:
        if effect.trigger is not Trigger.ON_PLAY:
            activeCards.append(card)
        else:
            match effect.target:
                case Target.SELF:
                    effect.onTrigger(player_self)
                case Target.OPPONENT:
                    effect.onTrigger(opponent)
                case Target.SELF_GAME_BOARD:
                    effect.onTrigger(player_self.game_board)
                case Target.OPPONENT_GAME_BOARD:
                    effect.onTrigger(opponent.game_board)

def deactivateCard(card: Card):
    for effect in card.effects:
        if effect.trigger is Trigger.ON_DESTROY:
            match effect.target:
                case Target.SELF:
                    effect.onTrigger(player_self)
                case Target.OPPONENT:
                    effect.onTrigger(opponent)
                case Target.SELF_GAME_BOARD:
                    effect.onTrigger(player_self.game_board)
                case Target.OPPONENT_GAME_BOARD:
                    effect.onTrigger(opponent.game_board)

    activeCards.remove(card)
    
def playCard(cardIdx: int, player: int):
    if player == 1:
        card = player_self.playCard(cardIdx)
        activateCard(card)
    else:
        card = opponent.playCard(cardIdx)
        activateCard(card)

def trigger(trigger: Trigger):
    for card in activeCards:
        for effect in card.effects:
            if effect.trigger is trigger:
                target = Component("base")

                match effect.target:
                    case Target.SELF:
                        target = player_self
                    case Target.OPPONENT:
                        target = opponent
                    case Target.SELF_GAME_BOARD:
                        effect.onTrigger(player_self.game_board)
                    case Target.OPPONENT_GAME_BOARD:
                        effect.onTrigger(opponent.game_board)

                effect.onTrigger(target)

def checkLifetimes(lifetime: Lifetime):
    for card in activeCards:
        if card.lifetime is lifetime:
            deactivateCard(card)

def printActiveCards():
    print("Active cards:")
    for card in activeCards:
        print(card.name)
    print()

def run():
    setup()

    while True:
        printActiveCards()
        checkLifetimes(Lifetime.NEXT_ROUND_START)
        printInstructions()

        if player_self.is_active and len(player_self.hand) > 0:
            key = readInput()

            if key == "q":
                break
            
            if int(key):
                playCard(int(key), 1)
                checkLifetimes(Lifetime.PLAYER_TURN_END)

        if opponent.is_active and len(opponent.hand) > 0:
            opponentPlay()
            checkLifetimes(Lifetime.OPPONENT_TURN_END)

        checkLifetimes(Lifetime.ROUND_END)

        if len(player_self.hand) <= 0 and len(opponent.hand) <= 0:
            break

    print("Bye bye")

if __name__ == "__main__":
    run()
