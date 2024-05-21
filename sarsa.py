import math
from methods import BlackjackAgent, play_blackjack

class SarsaAgent(BlackjackAgent):
    def update_q_value(self, state, action, reward, alpha):

        sa = self.get_state_action(state, action)
        self.action_counts[sa] += 1 
        alpha = 1/(self.action_counts[sa]+1)
        
        # just_future = self.q_values[sa]
        if action == "STAND":
            self.q_values[sa] += alpha * (reward - self.q_values[sa])
        else:
            self.q_values[sa] += alpha * (reward + )

first_start = lambda k: 1/10
second_start = lambda k: 1/k
third_start = lambda k:math.exp(-k / 1000)
fourth_start = lambda k:math.exp(-k / 10000)

play_blackjack(SarsaAgent, 100000, "is counted in update_q_value", first_start)