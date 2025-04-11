from component import Component
from player import Player

def freezePlayer(player: Component):
    if isinstance(player, Player):
        player.__class__ = Player
        player.is_active = False
def unfreezePlayer(player: Component):
    if isinstance(player, Player):
        player.__class__ = Player
        player.is_active = True


