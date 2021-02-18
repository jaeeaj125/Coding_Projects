import random

# build the dictionaries for constructing poker desk
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_list = []
        for i in self.deck:
            deck_list.append(i.rank + ' of ' + i.suit)
        # return the string showing all cards in the desk
        return '\n'.join(deck_list)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 1:
            return self.value - 10  # return Ace's value = 1, but the self.value doesn't change
        else:
            return self.value  # return Ace's value = 11


class Chips:

    def __init__(self, total=100):
        self.total = total  # 100 is set to be default value or it can be supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(player_chip):

    print(f'You have {player_chip.total} chips now.')
    while True:
        try:
            player_bet = int(input('Please enter your bet: '))
        except:
            print('The bet you provide is not acceptable, please try again.')
        else:
            if player_bet > player_chip.total:
                print('No enough ammount for this bet, please try again.')
            elif player_bet <= 0:
                print('Invalid bet, please enter a postive integer.')
            else:
                player_chip.bet = player_bet
                break


def hit(deck, hand):

    hand.add_card(deck.deal())


def hit_or_stand(deck, hand):

    global playing  # to control an upcoming while loop
    while True:
        reply = input('Hit or Stand? (h/s)? ').lower()
        if reply.isalpha() and reply == 'h':
            hit(deck, hand)
            print('You choose to HIT.')
            break
        elif reply.isalpha() and reply == 's':
            print('\nYou choose to STAND')
            playing = False
            break
        else:
            pass


def show_some(player, dealer):

    print("Show current card.")
    print("\nDealer's card:\n{}".format(dealer.cards[0]))
    for i in range(len(dealer.cards)-1):
        print('Hidden')
    print("\nPlayer's card:")
    for card in player.cards:
        print(card)


def show_all(player, dealer):

    print("Show all card.")
    print("\nDealer's card:")
    for card in dealer.cards:
        print(card)
    print("\nPlayer's card:")
    for card in player.cards:
        print(card)

# following are the consequences that the game will get


def player_busts(player, dealer, player_chip):
    print(f'\nYour value is {player.value} and exceeds 21, the dealer wins.')
    print(f'You lost {player_chip.bet} bet.')
    player_chip.lose_bet()


def player_wins(player, dealer, player_chip):
    print(
        f"\nYour value is {player.value} and dealer's value is {dealer.value}, you win!")
    print(f'You got {player_chip.bet} bet.')
    player_chip.win_bet()


def dealer_busts(player, dealer, player_chip):
    print(f"\nDealer's value is {dealer.value} and exceeds 21, you win!")
    print(f'You got {player_chip.bet} bet.')
    player_chip.win_bet()


def dealer_wins(player, dealer, player_chip):
    print(
        f"\nYour value is {player.value} and dealer's value is {dealer.value}, you lose.")
    print(f'You lost {player_chip.bet} bet.')
    player_chip.lose_bet()


def push(player, dealer):
    print(
        f"\nYour value is {player.value} and dealer's value is {dealer.value}, it's a push!")
    print('Nothing change for your chips.')


# Main Code
playing = True
play_round = 0

while True:
    play_round += 1

    # Print an opening statement
    if play_round == 1:
        print('Welcome to the BLACKJACK GAME!\n')

    # Create & shuffle the deck, deal two cards to each player
    dealer = Hand()
    player = Hand()
    deck = Deck()
    deck.shuffle()
    for i in range(0, 2):
        dealer.add_card(deck.deal())
        player.add_card(deck.deal())

    # Set up the Player's chips
    if play_round == 1:
        player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.adjust_for_ace() > 21:
            player_busts(player, dealer, player_chips)
            show_all(player, dealer)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while dealer.value < 17 and player.adjust_for_ace() <= 21:
        dealer.add_card(deck.deal())
        print("Dealer's value is smaller 17, draw one more card.")

    # Show all cards
    show_all(player, dealer)

    # Run different winning scenarios
    if dealer.value > 21 and player.adjust_for_ace() <= 21:
        dealer_busts(player, dealer, player_chips)
    elif player.value > dealer.value and player.adjust_for_ace() <= 21:
        player_wins(player, dealer, player_chips)
    elif player.value < dealer.value and player.adjust_for_ace() <= 21:
        dealer_wins(player, dealer, player_chips)
    elif player.value == dealer.value and player.adjust_for_ace() <= 21:
        push(player, dealer)
    else:
        pass

    # Inform Player of their chips total
    print(f'You have {player_chips.total} chips now.')

    # Ask to play again
    reply = ''
    while True and player_chips.total != 0:

        reply = input('Play one more round or not? (y/n)').lower()
        if reply == 'y' or reply == 'n':
            break
        else:
            print('Invalid input, please try again.')

    if reply == 'y':
        playing = True
    elif player_chips.total == 0:
        print("You don't have any chip now.")
        break
    else:
        print("Thanks for your playing, see you next time!")
        break
