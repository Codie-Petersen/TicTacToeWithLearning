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

def get_best_move(possible_moves: Dict[str, object]):
    """Get the best move random on a tie."""
    best_move = []
    best_rewards = []
    for move in possible_moves.keys():
        reward = possible_moves[move]["reward"]
        if len(best_move) == 0:
            best_move.append(move)
            best_rewards.append(reward)
            continue
        if reward > best_rewards[0]:
            best_move = [move]
            best_rewards = [reward]
        elif reward == best_rewards[0]:
            best_move.append(move)
            best_rewards.append(reward)

    best_move = random.choice(best_move)
    return possible_moves[best_move]["index"]

def load_agent(brain_file, marker):
    """Load an agent from a brain file."""
    with open(brain_file, "r") as f:
        brain = json.load(f)
    agent = Agent(marker=marker)
    agent.brain.reward_table = brain
    print(f"Loaded agent {marker} from brain file {brain_file}")
    return agent

def self_play_loop(epochs: int, load_brains: bool=True, debug: bool=False):
    """Loop for self play."""
    board = Board()
    agent1 = Agent(marker="X")
    agent2 = Agent(marker="O")

    if load_brains:
        brain_file = ".\\brain1.json"
        agent1 = load_agent(brain_file, "X")
        brain_file = ".\\brain2.json"
        agent2 = load_agent(brain_file, "O")

    for epoch in tqdm(range(epochs)):
            board.reset()
            while not board.is_game_over():
                current_player = agent1 if board.last_player == agent2.marker else agent2
                moves = current_player.get_possible_moves_experimental()
                move = random_weighted_move(moves)
                board.make_move(move)
                board_move = board.get_board_state()
                agent1.add_move(board_move)
                agent2.add_move(board_move)
                #Check if the last move blocked a win and reward the blocking player
                if board.check_if_last_move_blocked_win():
                    if board.last_player == agent1.marker:
                        agent1.calculate_reward(0.5, False)
                        agent2.calculate_reward(0, False)
                    else:
                        agent1.calculate_reward(0, False)
                        agent2.calculate_reward(0.5, False)
            winner = board.get_winner()
            if winner == agent1.marker:
                agent1.calculate_reward(1)
                agent2.calculate_reward(-0.33)
            elif winner == agent2.marker:
                agent1.calculate_reward(-0.33)
                agent2.calculate_reward(1)
            else:
                agent1.calculate_reward(0.2)
                agent2.calculate_reward(0.2)
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

def play_human(brain_file: str):
    board = Board()

    #Load brain
    with open(brain_file, "r") as f:
        brain = json.load(f)
    agent = Agent(marker="O")
    agent.brain.reward_table = brain

    #Make loop for human and computer player
    while True:
        board.reset()
        while not board.is_game_over():
            if board.last_player == agent.marker or board.last_player == None:
                #Human player
                board.print_board()
                print("Your turn")
                move = int(input("Enter move: "))
            else:
                #Computer player
                moves = agent.get_possible_moves_experimental()
                move = get_best_move(moves)
            board.make_move(move)
            board_move = board.get_board_state()
            agent.add_move(board_move)
        winner = board.get_winner()
        if winner == agent.marker:
            print("Computer wins!")
        elif winner == None:
            print("Draw!")
        else:
            print("You win!")
        board.print_board()
        input("Press enter to continue...")

if __name__ == "__main__":
    DEBUG = False
    SELF_PLAY = input("Self play? (y/n): ") == "y"

    if SELF_PLAY:
        LOAD_BRAINS = input("Load brains? (y/n): ") == "y"
        epochs = int(input("Number of epochs: "))
        self_play_loop(epochs, LOAD_BRAINS)
    else:
        brain_file = input("Brain file: ")
        play_human(brain_file)

    
