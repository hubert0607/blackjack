from methods import BlackjackAgent, BlackjackGame, play_blackjack
import math

#Exploring Starts and 1/k in no exploring starts is literally the same in both cases we end up with first value beaing totally random one cus 1/1 is 1

# to do zrobienia i to jest ten nasz epsilon

exploring_start = lambda k: 1/k
thousand = lambda k:math.exp(-k / 1000)
ten_thousand = lambda k:math.exp(-k / 10000)


#i teraz po prostu sobie powywoluje tutaj montecarlosy

print(play_blackjack(BlackjackAgent, 100000, 0.1, exploring_start))