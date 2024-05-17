import random
from collections import defaultdict

class Deck:
    def __init__(self):
        self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            raise ValueError("All cards have been drawn")
        return self.cards.pop()

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_hand = [self.deck.draw_card()]
        

    def player_action(self, action):
        if action == 'HIT':
            self.player_hand.append(self.deck.draw_card())
        elif action == 'STAND':
            while self.__sum_hand(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.draw_card())

    def __sum_hand(self, hand):
        total = sum(hand)
        if 1 in hand and total + 10 <= 21:
            return total + 10
        return total

    def get_state(self):
        player_sum = self.__sum_hand(self.player_hand)
        dealer_card = self.dealer_hand[0]
        use_ace = 1 in self.player_hand and self.__sum_hand(self.player_hand) <= 21
        return player_sum, dealer_card, use_ace

    def get_result(self):
        player_sum = self.__sum_hand(self.player_hand)
        dealer_sum = self.__sum_hand(self.dealer_hand)
        if player_sum > 21:
            return -1  # Player loses
        if dealer_sum > 21 or player_sum > dealer_sum:
            return 1  # Player wins
        if player_sum < dealer_sum:
            return -1  # Dealer wins
        return 0  # Draw


class BlackjackAgent:
    def __init__(self):
        # self.steps = 0
        self.q_values = defaultdict(float)
        self.action_counts = defaultdict(int) #huj wie po co to
        self.state_count = defaultdict(int)

    def __get_state_action(self, state, action):
        return state + (action,)

    def update_q_value(self, state, action, reward, alpha):
        # self.steps = 0
        sa = self.__get_state_action(state, action)
        self.action_counts[sa] += 1
        self.q_values[sa] += alpha * (reward - self.q_values[sa])
        # self.steps = self.action_counts[sa]

    def choose_action(self, state, epsilon):
        # self.steps += 1
        
        player_sum, dealer_card, use_ace = state
        if player_sum < 12:

            return 'HIT'
        if player_sum == 21:
            return 'STAND'

        if random.random() < epsilon:
            return random.choice(['HIT', 'STAND'])
        hit_value = self.q_values[self.__get_state_action(state, 'HIT')]
        stand_value = self.q_values[self.__get_state_action(state, 'STAND')]
        return 'HIT' if hit_value > stand_value else 'STAND'

    def montecarlo_states_counts(self, state):
        
        self.state_counts[state] += 1
        return self.state_counts[state]


def play_blackjack(black_agent,episodes, alpha, epsilon_function):
    agent = black_agent()
    for _ in range(episodes):
        game = BlackjackGame()
        state = game.get_state()
        action = ""
        while action != "STAND":
            
            k = agent.montecarlo_states_counts(state)
            action = agent.choose_action(state, epsilon_function(k)) 

            game.player_action(action)
            state = game.get_state()
            if action == 'STAND' or state[0] > 21: #state[0] means player sum
                reward = game.get_result()
                agent.update_q_value(state, action, reward, alpha)

    return agent.q_values    



    
