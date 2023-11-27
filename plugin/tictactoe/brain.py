"""
A simple memoization based reward table for TicTacToe.
The reward table is a dictionary with the key being the board state and the value being the reward.
Inside each board state, you add the next board state as the key and the reward as the value.
The idea is to nest moves inside of moves to create a tree of moves.
This is important because there are multiple ways to get to the same board state, in particular the
end game states. You want to ensure that you are rewarding the correct path to the end game state.
"""
class Brain:

    def __init__(self):
        self.reward_table = {}
        self.past_moves = []
        self.falloff = 2 # How much to reduce the reward by each move

    def add_move(self, board_state):
        """
        Add a move to the reward table.

        :param board_state: The board state as a stirng of 9 characters.
        """
        self.past_moves.append(board_state)
        self._set_nested_rewards(self.past_moves)

    def caclulate_reward(self, reward):
        """
        Calculate the reward, add it to the reward table, and reset the past moves.

        :param reward: The reward to add to the reward table.
        """
        #Calculate the rewards per past move
        rewards = []
        for i in range(len(self.past_moves)):
            temp_reward = reward / (self.falloff ** i)
            rewards.append(temp_reward)
        rewards.reverse()

        #Add the rewards to the reward table
        self._set_nested_rewards(self.past_moves, rewards)
        self.past_moves = []
    
    def _set_nested_rewards(self, keys, rewards=0):
        """
        Set a value in a nested dictionary given a list of keys.

        :param keys: A list of keys to traverse the nested dictionary.
        :param value: The value to set at the final key.
        """
        print(rewards)
        current_level = self.reward_table
        for k, key in enumerate(keys):  # Go to the second last key
            print(keys, k)
            if key not in current_level:
                current_level[key] = {}
            if rewards != 0:
                current_level[key]["reward"] = (current_level[key].get("reward", 0) + rewards[k])/2
            else:
                current_level[key]["reward"] = current_level[key].get("reward", 0)
            current_level = current_level[key]

