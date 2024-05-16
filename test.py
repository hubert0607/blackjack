import random
import numpy as np
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
        self.player_hand = []
        self.dealer_hand = []
        self.reset_game()

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_hand = [self.deck.draw_card()]

    def player_action(self, action):
        if action == 'HIT':
            self.player_hand.append(self.deck.draw_card())
        elif action == 'STAND':
            while self.sum_hand(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.draw_card())

    def sum_hand(self, hand):
        total = sum(hand)
        if 1 in hand and total + 10 <= 21:
            return total + 10
        return total

    def get_state(self):
        player_sum = self.sum_hand(self.player_hand)
        dealer_card = self.dealer_hand[0]
        use_ace = 1 in self.player_hand and self.sum_hand(self.player_hand) <= 21
        return player_sum, dealer_card, use_ace

    def get_result(self):
        player_sum = self.sum_hand(self.player_hand)
        dealer_sum = self.sum_hand(self.dealer_hand)
        if player_sum > 21:
            return -1  # Player loses
        if dealer_sum > 21 or player_sum > dealer_sum:
            return 1  # Player wins
        if player_sum < dealer_sum:
            return -1  # Dealer wins
        return 0  # Draw

class RLAgent:
    def __init__(self):
        self.Q = defaultdict(lambda: np.zeros(2))  # Q-values
        self.N = defaultdict(int)  # State-action counts

    def choose_action(self, state, epsilon):
        if random.random() < epsilon:
            return random.choice([0, 1])  # 0: HIT, 1: STAND
        else:
            return np.argmax(self.Q[state])

    def update_Q(self, state, action, reward, alpha):
        self.N[state, action] += 1
        self.Q[state][action] += alpha * (reward - self.Q[state][action])

class MonteCarlo:
    def __init__(self, agent):
        self.agent = agent

    def run_episode(self, epsilon):
        game = BlackjackGame()
        episode = []
        state = game.get_state()
        while True:
            action = self.agent.choose_action(state, epsilon)
            game.player_action('HIT' if action == 0 else 'STAND')
            next_state = game.get_state()
            episode.append((state, action))
            if action == 1 or game.sum_hand(game.player_hand) > 21:
                reward = game.get_result()
                break
            state = next_state
        for state, action in episode:
            self.agent.N[state, action] += 1  # Ensure count is non-zero
            self.agent.update_Q(state, action, reward, 1/self.agent.N[state, action])

def run_monte_carlo(agent, num_episodes, epsilon):
    mc = MonteCarlo(agent)
    for episode in range(num_episodes):
        mc.run_episode(epsilon)

# Example usage:
agent = RLAgent()
run_monte_carlo(agent, num_episodes=1000, epsilon=0.1)

# To check some Q-values
print(list(agent.Q.items())[:10])  # Display only the first 10 Q-values for brevity
