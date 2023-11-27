from plugin.tictactoe.agent import Agent
from plugin.tictactoe.game import Board
from typing import Dict
from tqdm import tqdm
import numpy as np
import random
import json

def modified_sigmoid(x, epsilon=0.01):
    return 1 / (1 + np.exp(-x)) + epsilon

def min_max_normalize(x, min, max):
    if min == max:
        return 0
    return (x - min) / (max - min)

def random_weighted_move(possible_moves: Dict[str, object]):
    """Get a random weighted move."""
    moves = []
    rewards = []
    for move in possible_moves:
        moves.append(possible_moves[move]["index"])
        rewards.append(possible_moves[move]["reward"])
    min_weight = min(rewards)
    max_weight = max(rewards)
    weights = [min_max_normalize(x, min_weight, max_weight) for x in rewards]
    weights = [modified_sigmoid(x) for x in weights]
    return random.choices(moves, weights=weights)[0]

def load_agent(brain_file, marker):
    """Load an agent from a brain file."""
    with open(brain_file, "r") as f:
        brain = json.load(f)
    agent = Agent(marker=marker)
    agent.brain.reward_table = brain
    print(f"Loaded agent {marker} from brain file {brain_file}")
    return agent

if __name__ == "__main__":
    DEBUG = False
    SELF_PLAY = False
    if input("Load brain? (y/n): ") == "y":
        brain_file = ".\\brain1.json"
        agent1 = load_agent(brain_file, "X")
        brain_file = ".\\brain2.json"
        agent2 = load_agent(brain_file, "O")
    else:
        agent1 = Agent(marker="X")
        agent2 = Agent(marker="O")
    board = Board()
    epochs = 100000

    if SELF_PLAY:
        for epoch in tqdm(range(epochs)):
            board.reset()
            while not board.is_game_over():
                current_player = agent1 if board.last_player == agent2.marker else agent2
                moves = current_player.get_possible_moves()
                move = random_weighted_move(moves)
                board.make_move(move)
                board_move = board.get_board_state()
                agent1.add_move(board_move)
                agent2.add_move(board_move)
            winner = board.get_winner()
            if winner == agent1.marker:
                agent1.calculate_reward(1)
                agent2.calculate_reward(-1)
            elif winner == agent2.marker:
                agent1.calculate_reward(-1)
                agent2.calculate_reward(1)
            else:
                agent1.calculate_reward(0)
                agent2.calculate_reward(0)
            if DEBUG:
                print(f"Epoch: {epoch} Winner: {winner}")
                board.print_board()
                input("Press enter to continue...")
        print("Training complete")
        print("Saving brains...")

        with open("brain1.json", "w") as f:
            brain = json.dump(agent1.brain.reward_table, indent=4, fp=f)
        with open("brain2.json", "w") as f:
            brain = json.dump(agent2.brain.reward_table, indent=4, fp=f)
        print("Brains saved")
    else:
        #Load brain
        with open("brain1.json", "r") as f:
            brain = json.load(f)
        agent1.brain.reward_table = brain

        #Make loop for human and computer player
        while True:
            board.reset()
            while not board.is_game_over():
                if board.last_player == agent2.marker or board.last_player == None:
                    #Human player
                    board.print_board()
                    print("Your turn")
                    move = int(input("Enter move: "))
                    board.make_move(move)
                else:
                    #Computer player
                    moves = agent2.get_possible_moves()
                    move = random_weighted_move(moves)
                    board.make_move(move)
                board_move = board.get_board_state()
                agent2.add_move(board_move)
            winner = board.get_winner()
            if winner == agent2.marker:
                print("Computer wins!")
            elif winner == None:
                print("Draw!")
            else:
                print("You win!")
            board.print_board()
            input("Press enter to continue...")