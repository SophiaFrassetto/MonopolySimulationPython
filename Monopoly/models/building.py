# build-in imports
from dataclasses import dataclass

# project imports
from .player import Player


@dataclass
class Building:
    name: str
    cost: int
    renting: int
    owner: Player = None

    def buy(self, player: Player):
        self.owner = player
        self.owner.money -= self.cost

    def rent(self, player: Player):
        player.money -= self.renting
        self.owner.money += self.renting

    def revoke(self):
        self.owner = None

    def has_owner(self):
        return True if self.owner else False

