# build-in imports 
import argparse
from random import getrandbits
from random import randint
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# project imports
from models import Behavior
from models import PlayerProfile
from models import Building
from table_game import TableGame


def arguments():
    parser = argparse.ArgumentParser(description='This is the simulation of a simple real estate bank')
    parser.add_argument('--simulations', type=int, default=300, help='Total simulations')
    parser.add_argument('--reward', type=int, default=100, help='Reward for player passed in first board position')
    parser.add_argument('--money', type=int, default=300, help='Initial money')
    parser.add_argument('--max_rounds', type=int, default=1000, help='Max rounds')
    parser.add_argument('--max_workers', type=int, default=8, help='Max workers for threads')

    return parser.parse_args()


# create behaviors and rules
behaviors = {
    "impulsive": Behavior(name="impulsive", rule=lambda p, b: True),
    "demanding": Behavior(name="demanding", rule=lambda p, b: True if b.renting > 50 else False),
    "cautious": Behavior(name="cautious", rule=lambda p, b: True if int(p.money - b.cost) >= 80 else False),
    "aleatory": Behavior(name="aleatory", rule=lambda p, b: bool(getrandbits(1))),
}

# create a players
players_profiles = [
    PlayerProfile(name="player1-impulsive", behavior=behaviors['impulsive']),
    PlayerProfile(name="player2-demanding", behavior=behaviors['demanding']),
    PlayerProfile(name="player3-cautious", behavior=behaviors['cautious']),
    PlayerProfile(name="player4-aleatory", behavior=behaviors['aleatory']),
]

# create a board aleatory
board = [Building(name=f"Casa-{x}", cost=randint(250, 1500),renting=randint(25, 100)) for x in range(1, 21)]


if __name__ == '__main__':
    args = arguments()

    with ThreadPoolExecutor(max_workers=args.max_workers) as executer:
        simulations = []
        futures = {}

        for _ in range(1, args.simulations+1):
            future = (
                executer.submit(
                    TableGame,
                    players_profiles,
                    board,
                    args.money,
                    args.reward,
                    args.max_rounds,
                )
            )

            futures[future] = _

        for future in as_completed(futures):
            game = future.result()

            # append finish result
            simulations.append({"total_rounds": game.total_rounds()-1})
        
        print(f"Total simulations: {args.simulations}")


        # get all rounds finish in Time Out 
        total_timeout = len([x for x in simulations if x['total_rounds'] == args.max_rounds])
        print(f"Total rounds finish with Time Out: {total_timeout}")

        # get average rounds
        avg = lambda x: sum(x) / len(x)
        average_rounds = avg([x['total_rounds'] for x in simulations])
        print(f"Average of rounds: {int(average_rounds)}")

        behaviors_win = {
            "impulsive": [0, 0],
            "demanding": [0, 0],
            "cautious": [0, 0],
            "aleatory": [0, 0],
        }
        # get percent for behavior player
        for player in players_profiles:
            behaviors_win[player.behavior.name][0] += player.win
            behaviors_win[player.behavior.name][1] += player.lose

        behavior_most_win = None
        for n, v in behaviors_win.items():
            print(f'{n} win: {v[0]} / {round((v[0] / args.simulations) * 100, 2)}% | lose: {v[1]} / {round((v[1] / args.simulations) * 100, 2)}%')
            if not behavior_most_win:
                behavior_most_win = n
            elif behaviors_win[n][0] > behaviors_win[behavior_most_win][0]:
                behavior_most_win = n

        # get behavior with more wins
        print(f"{behavior_most_win} most win with {behaviors_win[behavior_most_win][0]} / {round((behaviors_win[behavior_most_win][0] / args.simulations) * 100, 2)}%")
