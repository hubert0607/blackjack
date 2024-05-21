from methods import BlackjackAgent, play_blackjack_montecarlo
import math

#Exploring Starts and 1/k in no exploring starts is literally the same in both cases we end up with first value beaing totally random one cus 1/1 is 1

# to do zrobienia i to jest ten nasz epsilon


class CarloAgent(BlackjackAgent):
    def update_q_value(self, sa, reward):

        self.action_counts[sa] += 1
        # just_future = self.q_values[sa]

        self.q_values[sa] += reward/self.action_counts[sa]






exploring_start = lambda k: 1/k
thousand = lambda k:math.exp(-k / 1000)
ten_thousand = lambda k:math.exp(-k / 10000)



print(play_blackjack_montecarlo(CarloAgent, 100000, exploring_start))