# Blackjack Game
import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
from IPython.display import clear_output

class cards:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f" {self.rank} of {self.suit}"

class deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append((rank, suit))

    def __str__(self):
        return f"The deck has {len(self.deck)} cards left"

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

class hand:

    def __init__(self):
        self.cards = []
        self.aces = 0
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        if card[0] == "Ace":
            self.aces += 1
        self.value += values[card[0]]
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def show_cards(self, player):
        print(f"\n{player} cards: ")
        for card in self.cards:
            test_card = cards(card[0], card[1])
            print(test_card)
        print(f"\nValue of Hand: {self.value}")

    def show_some_cards(self, player):
        print(f"\n{player} cards:")
        print(" Hidden")
        for card in self.cards[1:]:
            test_card = cards(card[0], card[1])
            print(test_card)

class chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

    def take_bet(self):
        print(f"You have {self.total} chips")
        while True:
            try:
                self.bet = int(input("Please enter the amount of chips you would like to bet: "))
                if self.bet > self.total:
                    print("\n" + "You can only bet as many chips as you have!")
                elif self.bet <= 0:
                    print("\n" + "You must bet an amount greater than zero!")
                else:
                    break
            except:
                print("Please enter the amount of chips as an integer!")

    def __str__(self):
        return f"You have {self.total} chips."

def hit_or_stand():
    answer = "test"
    while answer not in ("HIT", "STAND"):
        answer = input("Would you like to hit or stand? ").upper()
        if answer not in ("HIT", "STAND"):
            print("\n" + "Please enter your answer as hit or stand!")
    return answer

def deal_cards(hand, deck):
    hand.cards.append(deck.deal())
    hand.value_hand()

def display_cards(dealer, player):
    clear_output()
    dealer.show_some_cards("Dealer's")
    player.show_cards("Your")

def win_check(x, y, z, answer = "HIT"):

    if x.value == 21: # blackjack check
        game_over(x, y)
        print("You have a blackjack! You have won your bet!")
        z.win_bet()
        return "over"
    elif y.value == 21:
        game_over(x, y)
        print("The dealer has a blackjack! You have lost your bet!")
        z.lose_bet()
        return "over"

    if x.value > 21: # bust check
        game_over(x, y)
        print("You have busted! You have lost your bet!")
        z.lose_bet()
        return "over"
    elif y.value > 21:
        game_over(x, y)
        print("The dealer has busted! You have won your bet!")
        z.win_bet()
        return "over"

    if x.value <= 21 and answer == "STAND": # other type of wins check
        if y.value > x.value:
            game_over(x, y)
            print("The dealer beat you! You have lost your bet!")
            z.lose_bet()
            return "over"
        elif x.value > y.value:
            game_over(x, y)
            print("You beat the dealer! You have won your bet!")
            z.win_bet()
            return "over"
        else:
            game_over(x, y)
            print("It's a push! Your bet has been returned!")
            return "over"

def game_over(x, y):
    clear_output()
    y.show_cards("Dealer's")
    x.show_cards("Your")

def start_game():
    player = chips()

    while True:
        status = "play"
        player_hand = hand()
        dealer_hand = hand()

        game_deck = deck()
        game_deck.shuffle()
    
        player.take_bet()

        for i in range(0,2):
            player_hand.add_card(game_deck.deal())
            dealer_hand.add_card(game_deck.deal())
    
        dealer_hand.show_some_cards("Dealer's")
        player_hand.show_cards("Your")

        status = win_check(player_hand, dealer_hand, player)
        
        while status != "over":

            answer = hit_or_stand()
        
            if answer == "HIT":
                player_hand.add_card(game_deck.deal())
        
            while dealer_hand.value <= 17:
                dealer_hand.add_card(game_deck.deal())
                break

            if answer == "HIT":
                display_cards(dealer_hand, player_hand)

            status = win_check(player_hand, dealer_hand, player, answer)

        if player.total == 0:
            print("You have no more chips! \nGAME OVER")
            break
        else:
            prompt = input("Would you like to play again? YES or NO: ").upper()
            if prompt not in ("YES", "NO"): 
                while True:
                    prompt = input("Please enter your answer as YES or NO: ").upper()
                    if prompt in ("YES", "NO"):
                        break

            if prompt == "YES":
                clear_output()
                continue
            else:
                break

if __name__ == "__main__":
    start_game()
