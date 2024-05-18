import math
from methods import BlackjackAgent, play_blackjack

class QLearningAgent(BlackjackAgent):
    def update_q_value(self, state, action, reward, alpha):
        sa = self.__get_state_action(state, action)
        self.action_counts[sa] += 1
        alpha = 1 / (self.action_counts[sa] + 1)
        future_rewards = [self.q_values[self.__get_state_action(state, a)] for a in ['HIT', 'STAND']]
        self.q_values[sa] += alpha * (reward + max(future_rewards) - self.q_values[sa])
