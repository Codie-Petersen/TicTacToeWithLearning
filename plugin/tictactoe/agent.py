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
        self._set_rewards(self.past_moves)

    def caclulate_reward(self, reward, reset=True):
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
        self._set_rewards(self.past_moves, rewards)
        if reset:
            self.past_moves = []
    
    def get_current_board_state(self):
        """
        Get the current board state.

        :return: The current board state.
        """
        if len(self.past_moves) == 0:
            return "_" * 9
        return self.past_moves[-1]

    def get_board_state_rewards(self):
        """
        Get the rewards for the current board state based on the past moves.

        :return: The dictionary of rewards for the current board state.
        """
        current_level = self.reward_table
        for key in self.past_moves:
            if key not in current_level:
                return {}
            current_level = current_level[key]
        return current_level
    
    def get_board_state_rewards_experimental(self):
        """
        Unlike the nested state reward table, this one is flat.
        """
        return self.reward_table
    
    def _set_nested_rewards(self, keys, rewards=0):
        """
        Set a value in a nested dictionary given a list of keys.

        :param keys: A list of keys to traverse the nested dictionary.
        :param value: The value to set at the final key.
        """
        current_level = self.reward_table
        for k, key in enumerate(keys):  # Go to the second last key
            if key not in current_level:
                current_level[key] = {}
            if rewards != 0:
                current_level[key]["reward"] = (current_level[key].get("reward", rewards[k]) + rewards[k])/2
            else:
                current_level[key]["reward"] = current_level[key].get("reward", 0)
            current_level = current_level[key]

    def _set_rewards(self, keys, rewards=[0]):
        """
        A function to set the rewards of a given board state.

        :param keys: The keys to traverse the dictionary.
        :param value: The value to set the reward to.
        """
        if rewards == [0]:
            rewards = rewards*len(keys)
        key = "-".join(keys)
        for i in range(len(keys)):
            key = "-".join(keys[:-i])
            try:
                if key not in self.reward_table:
                    self.reward_table[key] = rewards[i]
                else:
                    self.reward_table[key] = (self.reward_table[key] + rewards[i])/2
            except:
                print("------------------")
                print(key)
                print(self.reward_table)
                print(rewards)
                print("------------------")
                raise Exception("Error")


class Agent:

    def __init__(self, marker: str, brain_file=None):
        self.brain = Brain()
        self.marker = marker
        self.goal = ""

    def add_move(self, board_state):
        """
        Add a move to the agent.

        :param board_state: The board state as a string of 9 characters.
        """
        self.brain.add_move(board_state)
    
    def calculate_reward(self, reward, reset=True):
        """
        Calculate the reward for the agent.

        :param reward: The reward to add to the agent.
        """
        self.brain.caclulate_reward(reward, reset)
    
    def set_goal(self):
        """
        From the reward table, set one of the best keys as the goal.
        
        :param goal: The goal to set for the agent.
        """
        rewards = self.brain.reward_table.copy()
        keys = list(rewards.keys())
        values = list(rewards.values())

        #Get the best reward
        best_reward = max(values)
        best_reward_index = values.index(best_reward)
        best_reward_key = keys[best_reward_index]
        self.goal = best_reward_key

    
    def get_possible_moves(self):
        """
        Get the possible moves for a given board.

        :param board: The board to get the possible moves for.
        :return: A list of possible moves.
        """
        board_state = self.brain.get_current_board_state()
        moves = [i for i, x in enumerate(board_state) if x == "_"] #Moves in board class style.
        #Create board state combinations based on the possible moves
        board_state_combinations = []
        
        for move in moves:
            board_combo = self._set_board_combo(board_state, move, self.marker)
            board_state_combinations.append(board_combo)

        #Dictionary of moves and rewards
        move_dict = {}
        rewards = self.brain.get_board_state_rewards()
        for move, combo in zip(moves, board_state_combinations):
            move_dict[combo] = { 
                "index": move, 
                "reward": rewards.get(combo, {}).get("reward", 0)
            }
        return move_dict
    
    def get_possible_moves_experimental(self):
        """
        Unlike the nested state reward table, this one is flat.
        """
        board_state = self.brain.get_current_board_state()
        temporal_state = "-".join(self.brain.past_moves)
        moves = [i for i, x in enumerate(board_state) if x == "_"] #Moves in board class style.
        #Create board state combinations based on the possible moves
        board_state_combinations = []
        
        for move in moves:
            board_combo = self._set_board_combo(board_state, move, self.marker)
            board_state_combinations.append(board_combo)

        #Dictionary of moves and rewards
        move_dict = {}
        rewards = self.brain.get_board_state_rewards_experimental()
        for move, combo in zip(moves, board_state_combinations):
            if temporal_state == "":
                temporal_key = combo
            else:
                temporal_key = f"{temporal_state}-{combo}"
            try:
                move_dict[temporal_key] = { 
                    "index": move, 
                    "reward": rewards.get(temporal_key, 0)
                }
            except:
                print("------------------")
                print(temporal_key)
                print(rewards)
                print("------------------")
                raise Exception("Error")

        return move_dict


    def _set_board_combo(self, board, move, marker):
        """
        Set a move on a board.

        :param board: The board to set the move on.
        :param move: The move to set.
        :param marker: The marker to set the move as.
        """
        board = ''.join([marker if i == move else char for i, char in enumerate(board)])
        return board
