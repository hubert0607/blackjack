import random

class Deck:
    def __init__(self):
        self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        random.shuffle(self.cards)

    def draw_card(self):
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

        if 1 in self.player_hand:
            use_ace = 1
        else:
            use_ace = 0

        return {"player_sum":player_sum, "dealer_card":dealer_card, "ace":use_ace}

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
    



