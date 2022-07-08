# build-in imports
from dataclasses import dataclass
from typing import List
from random import shuffle

# project imports
from models import PlayerProfile
from models import Player


@dataclass
class TableGame:
    players: List[PlayerProfile]
    board: dict
    initial_money: int = 300
    reward: int = 100
    max_rounds: int = 1000

    def __post_init__(self):
        self.rounds = 1

        self.start()

    def player_reward(self, player: Player):
        # the reward is for when the player passes the first board position again
        player.money += self.reward

    def set_position(self, player: Player, dice_value: int):
        current_position = player.position
        position = current_position + (dice_value)
        if position > len(self.board):
            position = position - len(self.board)
        return position-1

    def player_round(self, player_sequence: list, last_player: Player=None):
        # set player for the round
        if not last_player or last_player == player_sequence[-1]:
            return player_sequence[0]
        return player_sequence[player_sequence.index(last_player) + 1]

    def total_rounds(self):
        return self.rounds

    def check_player_win(self, player_sequence):
        if len(player_sequence) == 1:
            player_sequence[0].profile.win += 1
        else:
            player_win = None
            for player in player_sequence:
                if not player_win:
                    player_win = player
                    continue
                if player.money > player_win.money:
                    player_win.lose()
                    player_win = player
                else:
                    player.lose()
            player_win.profile.win += 1

    def start(self):
        # shuffle players
        shuffle(self.players)
        player_sequence = [Player(money=self.initial_money, profile=x) for x in self.players]

        last_player = None
        has_next_round =True
        while has_next_round:
            # check has_next_round
            if self.rounds > self.max_rounds or len(player_sequence) <= 1:
                has_next_round = False
                continue


            # set player round
            player = self.player_round(player_sequence, last_player)

            player_last_position = player.position

            # roll dice and set position in board
            player.position = self.set_position(player, player.roll_dice())

            # check if player passes in first board position again
            if player.position < player_last_position:
                self.player_reward(player)

            # build in player position
            building = self.board[player.position]

            # check if build has owner
            if building.has_owner():
                # collect rent
                building.rent(player)

            else:
                # check rule with player behavior
                if player.profile.behavior.rule(player, building):
    
                    # buy build
                    building.buy(player)
                    # check player lose
                    if player.check_lose():
        
                        # set lose
                        player.lose()
                        # remove player from sequence
                        player_sequence.pop(player_sequence.index(player))

                        # revoke all build for the player
                        for b in self.board:
                            if b.owner == player:
                                b.revoke()

            self.rounds += 1

        self.check_player_win(player_sequence)







