import random
from time import sleep
import time

# Implement a slow print for better game flow
def slow_print(string):
    for char in string:
        print(char, end='')
        time.sleep(0.03)
    print()

# Represents a single card with a value and suit
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    # Returns the blackjack value of the card
    def get_card_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10  # Face cards are worth 10
        elif self.value == 'A':
            return 11  # Aces are worth 11 initially
        else:
            return int(self.value)  # Numeric cards are worth their value

    # Returns the string representation of the card (e.g., "A♠")
    def get_output_string(self):
        return self.value + self.suit

# Represents a deck of cards
class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        for _ in range(num_decks):
            self.__merge_deck()
        random.shuffle(self.cards)

    # Adds a standard 52-card deck to the deck list
    def __merge_deck(self):
        for val in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
            # Unicode symbols for suits symbols
            for suit in ["\u2663", "\u2665", "\u2666", "\u2660"]:
                self.cards.append(Card(val, suit))

    # Draws a card from the deck, reshuffling if the deck is empty
    def draw(self):
        if len(self.cards) == 0:
            self.__merge_deck()
            random.shuffle(self.cards)
        return self.cards.pop(0)

# Represents a hand of cards for a player or dealer
class Hand:
    def __init__(self, card1, card2):
        self.cards = [card1, card2]

    # Adds a new card to the hand
    def add_card(self, card):
        self.cards.append(card)

    # Calculates the total score of the hand considering aces as 1 or 11
    # This was the hardest part of this assignment. Recognizing that first counting all Aces
    # as 11 first then reducing by 10 if needed to get under 22 will maximize the score first.
    def calculate_score(self):
        score = 0
        aces = 0

        for card in self.cards:
            value = card.get_card_value()
            if value == 11:
                aces += 1
            score += value

        # Adjusts score if it exceeds 21 and there are aces in the hand
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    # Prints the cards in the hand with a given prefix string
    def print_cards_internal(self, prefix_string):
        for card in self.cards:
            prefix_string += (card.get_output_string() + "  ")
        slow_print(prefix_string)

# Represents the dealer's hand
class DealerHand(Hand):
    # Prints the dealer's hand with one card hidden
    def print_cards_hidden(self):
        slow_print("Dealer Hand: XX  " + self.cards[1].get_output_string())

    # Prints all cards in the dealer's hand
    def print_cards(self):
        self.print_cards_internal("Dealer Hand: ")

# Represents the player's hand
# Can be extended for multiple players
class PlayerHand(Hand):
    def print_cards(self):
        self.print_cards_internal("Player Hand: ")

# Manages the player's turn, returns True if the player busts
def player_turn(player_hand, dealer_hand, deck):
    slow_print("=============== Player's Turn ===============")

    while True:
        print()
        dealer_hand.print_cards_hidden()
        player_hand.print_cards()
        slow_print("Player Score: " + str(player_hand.calculate_score()))
        print("\n")
        choice = input('"hit" or "stay"? ').lower()

        if choice in ["hit", "h"]:
            card = deck.draw()
            print("\nPlayer Hits! Draws: " + card.get_output_string() + "\n")
            player_hand.add_card(card)
        elif choice in ["stay", "s"]:
            print("\nPlayer Stays!\n")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        if player_hand.calculate_score() > 21:
            print("\nPlayer Busts!\n")
            return True

    return False

# Manages the dealer's turn, returns True if the dealer busts
def dealer_turn(dealer_hand, deck):
    slow_print("=============== Dealer's Turn ===============\n")

    dealer_hand.print_cards()
    slow_print("Dealer Score: " + str(dealer_hand.calculate_score()))

    while dealer_hand.calculate_score() < 16:
        card = deck.draw()
        dealer_hand.add_card(card)
        slow_print("Dealer Hits! Draws: " + card.get_output_string() + "\n")
        sleep(1)
        dealer_hand.print_cards()
        slow_print("Dealer Score: " + str(dealer_hand.calculate_score()))

        if dealer_hand.calculate_score() > 21:
            slow_print("\nDealer Busts!\n")
            return True

    slow_print("\nDealer Stays!\n")
    return False

# Prints the final state of the game
def print_final_state(player_hand, dealer_hand):
    slow_print("=============== Final Results ===============\n")
    dealer_hand.print_cards()
    slow_print("Dealer Score: " + str(dealer_hand.calculate_score()) + "\n")
    player_hand.print_cards()
    slow_print("Player Score: " + str(player_hand.calculate_score()))
    slow_print("\n")

# Main game loop
def main():
    deck = Deck()
    slow_print("Welcome to Blackjack!")
    slow_print("Rules:")
    slow_print("1. The goal is to get as close to 21 as possible without exceeding it.")
    slow_print("2. Face cards (J, Q, K) are worth 10 points; Aces are worth 11 or 1.")
    slow_print("3. On your turn, you can either 'hit' to draw another card or 'stay' to keep your current hand.")
    slow_print("4. The dealer must draw until they reach at least 17.")
    slow_print("5. If you go over 21, you bust and lose the round.")
    slow_print("6. The game will continue until you choose to stop. Enjoy!\n")

    dealer_wins = 0
    player_wins = 0

    while True:
        player_hand = PlayerHand(deck.draw(), deck.draw())
        dealer_hand = DealerHand(deck.draw(), deck.draw())

        if player_turn(player_hand, dealer_hand, deck):
            print_final_state(player_hand, dealer_hand)
            slow_print("Dealer wins! (Player Busted)")
            dealer_wins += 1
        elif dealer_turn(dealer_hand, deck):
            print_final_state(player_hand, dealer_hand)
            slow_print("Player wins! (Dealer Busted)")
            player_wins += 1
        else:
            print_final_state(player_hand, dealer_hand)
            if player_hand.calculate_score() > dealer_hand.calculate_score():
                slow_print("Player Wins!")
                player_wins += 1
            elif player_hand.calculate_score() < dealer_hand.calculate_score():
                slow_print("Dealer Wins!")
                dealer_wins += 1
            else:
                slow_print("It's a Tie!")

        slow_print("\nScore: Player " + str(player_wins) + " - Dealer " + str(dealer_wins))

        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again not in ["yes", "y"]:
            slow_print("Thanks for playing!")
            break
        print("\n")

# Main Driver
if __name__ == "__main__":
    main()
