'''
Angel Ordonez Retamar
AAI 551 Final Project
I pledge my honor that I have abided by the Stevens Honor System
'''

#for my final project I used the classes from lecture notes and made one additional class "CardGame" to make a game of blackjack
#for my attempt at the 10 bonus points I added a power up for getting 21 or winning twice in a row
#when this happens the player gets to peek at their facedown card


import random #import random to shuffle cards

class Card: #ripped straight from lecture notes, represents a single playing card
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"] #making suits 0-3
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"] #making ranks 1-13
    def __init__(self, suit = 0, rank = 2): #initializes card, defaults don't matter here
        self.suit = suit
        self.rank = rank
    def __str__(self): #makes the cards easy to read when printed
        return (self.rank_list[self.rank] + " of " + self.suit_list[self.suit])
    def __eq__(self, other): #compares cards based on rank and suit for equality
        return (self.rank == other.rank and self.suit == other.suit) 
    def __gt__(self, other): #compares the cards preferring higher higher suit first then higher rank
        if self.suit > other.suit:
            return True
        elif self.suit == other.suit:
            if self.rank > other.rank:
                return True
        return False

class Deck: #ripped straight from lecture notes, represents full deck of cards
    def __init__(self): #initializes the 52 card deck
        self.cards = []
        for i in range(4):
            for j in range(1, 14):
                self.cards.append(Card(i, j))
    def __str__(self): #returns the string list of cards nicely indented
        s = ""
        for i in range(len(self.cards)):
            s += i * " " + str(self.cards[i]) + "\n"
        return s
    def shuffle(self): #shuffles deck using random
        random.shuffle(self.cards)
    def pop_card(self): #removes and returns the top card of the deck
        return self.cards.pop()
    def is_empty(self): #checks if the deck is empty
        return len(self.cards) == 0
    def deal(self, hands, n_cards = 52): #deals n_cards evenly among a list of hands
        n_players = len(hands)
        for i in range(n_cards):
            if self.is_empty():
                break
            card = self.pop_card()
            current_player = i % n_players #even or odd flips every time ensures cards get delt back and forth betwen 2 players, it works for any number of players though
            hands[current_player].add_card(card) #0 or 1 player or dealer gets the popped card

class Hand(Deck): #ripped straight from lecture notes, represents player or dealer's hand which inherits from Deck
    def __init__(self, name = ""): ##overrides Deck.__init__ to include a name
        self.cards = []
        self.name = name
    def add_card(self, card): #adds cards into hand
        self.cards.append(card)
    def __str__(self): #string output, uses the deck printing method
        s = "Hand of " + self.name
        if self.is_empty():
            #hand inherits from Deck so it takes the method from Deck
            return s + " is empty"
        s += " contains \n" + Deck.__str__(self) #uses the print from Deck instead of this one
        return s

class CardGame:
    def __init__(self): 
        self.player_score = 0 #track the number of rounds the player won
        self.dealer_score = 0 #track the number of rounds the dealer won
        self.player_wins_in_a_row = 0 #gotta keep track cause 2 in a row = power up
        self.power_ups = 0 #track how many of power ups the player has available

    def get_hand_value(self, hand): #calculates the value of a hand
        value = 0 #total value
        aces = 0 #number of ases
        for card in hand.cards: #loop through each card in the hand
            if card.rank >= 10: #face cards count as ten
                value += 10
            elif card.rank == 1:  #aces aces are initally counted as 11
                aces += 1
                value += 11
            else: #other cards are worth their number
                value += card.rank
        while value > 21 and aces: #adjust the value of aces to 1 if the score is over 21
            value -= 10
            aces -= 1
        return value

    def play_round(self): #one full round of the game
        self.deck = Deck() #create a new deck
        self.deck.shuffle() #shuffle it
        self.player_hand = Hand("Player") #initialize player hand
        self.dealer_hand = Hand("Dealer") #initialize dealer hand
        print("\n====== New Round ======") #make it clear that this is a new round

        for _ in range(2): # Deal 2 cards each
            self.player_hand.add_card(self.deck.pop_card())
            self.dealer_hand.add_card(self.deck.pop_card())

        round_over = False #controls the game loop for the round
        while not round_over: 
            print("Dealer shows:", self.dealer_hand.cards[1]) #index 0 is hidden card, show the visible card for the dealer
            print("Your hand:") 
            for i, card in enumerate(self.player_hand.cards):
                if i == 0: #first card is hidden
                    print("  [Hidden card]")
                else: #all cards after the first are shown
                    print(" ", card)

            print(f"Power-ups available: {self.power_ups}") #display the number of power ups
            print("Choose an option:") #choose to hit or stay
            print("1. Hit")
            print("2. Stay")
            if self.power_ups > 0: #only show power up option when power ups are available
                print("3. Use power-up to reveal hidden card")

            choice = input("Enter choice: ").strip() #get the user's input
            if choice == "1": #hit: draw a card and add it to the player's hand
                new_card = self.deck.pop_card()
                print("\nYou drew:", new_card)
                self.player_hand.add_card(new_card)
                if self.get_hand_value(self.player_hand) > 21: #check if that card makes the player go over 21 = bust
                    print("You busted!")
                    self.dealer_score += 1
                    self.player_wins_in_a_row = 0
                    round_over = True
            elif choice == "2": #stay = the end of the player's turn
                round_over = True
            elif choice == "3" and self.power_ups > 0: #use the power up, tell the player what the hidden card is
                print("\nYour hidden card was:", self.player_hand.cards[0])
                self.power_ups -= 1
            else: #anything other than 1, 2, or 3 when power ups are available
                print("Invalid input.")

        # Dealer's turn, only happens if the player did not bust
        if self.get_hand_value(self.player_hand) <= 21: 
            print("\nDealer's turn.")
            while self.get_hand_value(self.dealer_hand) < 17: #dealer stays if they reach 17 or higher, they are smart
                new_card = self.deck.pop_card()
                print("Dealer draws:", new_card)
                self.dealer_hand.add_card(new_card)

        print("\n--- Final Hands ---") #show both final hands, total scores
        print("Your hand:")
        for card in self.player_hand.cards:
            print(" ", card)
        print("Total:", self.get_hand_value(self.player_hand))

        print("Dealer's hand:")
        for card in self.dealer_hand.cards:
            print(" ", card)
        print("Total:", self.get_hand_value(self.dealer_hand))

        #determine who wins
        player_val = self.get_hand_value(self.player_hand)
        dealer_val = self.get_hand_value(self.dealer_hand)

        if player_val > 21: #player busted
            print("You busted. Dealer wins.")
            self.dealer_score += 1
            self.player_wins_in_a_row = 0
        elif dealer_val > 21 or player_val > dealer_val or player_val == dealer_val: #player wins in a tie too, makes it easier
            print("You win!")
            self.player_score += 1
            self.player_wins_in_a_row += 1
            if player_val == 21 or self.player_wins_in_a_row >= 2: #give a power up if the player gets blackjack or 2 wins in a row
                print("You earned a power-up!")
                self.power_ups += 1
                self.player_wins_in_a_row = 0
        else: #dealer wins, reset wins in a row to 0
            print("Dealer wins.")
            self.dealer_score += 1
            self.player_wins_in_a_row = 0

        print(f"\nScore — You: {self.player_score} | Dealer: {self.dealer_score}") #show the running score

    def play(self): #game loop for playing multiple rounds
        print("Welcome to Blackjack!")
        while True:
            self.play_round()
            again = input("\nPlay another round? (y/n): ").strip().lower()
            if again != 'y':
                print("Thanks for playing!")
                break

# To run the game:
if __name__ == "__main__":
    game = CardGame()
    game.play()