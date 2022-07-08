# build-in imports
from dataclasses import dataclass
from random import randint


@dataclass
class Behavior:
    name: str
    rule: object


@dataclass
class PlayerProfile:
    name: str
    behavior: Behavior
    win: int = 0
    lose: int = 0


@dataclass
class Player:
    money: int
    profile: PlayerProfile
    position: int = 0

    def lose(self):
        self.profile.lose += 1

    def check_lose(self):
        if self.money < 0:
            return True
        return False

    def roll_dice(self):
        return randint(1, 6)