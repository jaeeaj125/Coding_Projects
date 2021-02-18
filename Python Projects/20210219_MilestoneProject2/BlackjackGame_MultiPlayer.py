import random

# build the dictionaries for constructing poker desk
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
player_created = 0


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
        # return the string showing all cards in the deck
        return '\n'.join(deck_list)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []      # start with an empty list
        self.value = 0       # start with zero value
        self.aces = 0        # add an attribute to keep track of aces
        self.playing = True  # provide a state of each player
        self.end = False     # determine whether the player got the result of the game

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 1:
            return self.value - 10  # return Ace's value = 1, but the self.value doesn't change
        else:
            return self.value       # return Ace's value = 11


class Chips:

    def __init__(self, total=100):
        self.total = total  # 100 is set to be default value or it can be supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(player_list, player_chip_list):

    global player_num
    for i in range(player_num):
        print(
            f'{player_list[i].name} has {player_chip_list[i].total} chips now.')
        while True:
            try:
                player_bet = int(input('Please enter your bet: '))
            except:
                print('The bet you provide is not acceptable, please try again.')
            else:
                if player_bet > player_chip_list[i].total:
                    print('No enough ammount for this bet, please try again.')
                elif player_bet <= 0:
                    print('Invalid bet, please enter a postive integer.')
                else:
                    player_chip_list[i].bet = player_bet
                    break


def hit(deck, player):

    player.add_card(deck.deal())


def hit_or_stand(deck, player_list):

    global playing  # to control an upcoming while loop
    global player_num
    for i in range(player_num):
        if player_list[i].playing:
            while True:
                reply = input(
                    f'\n{player_list[i].name}, you want to Hit or Stand? (h/s)? ').lower()
                if reply.isalpha() and reply == 'h':
                    hit(deck, player_list[i])
                    print(f'{player_list[i].name} choose to HIT.')
                    break
                elif reply.isalpha() and reply == 's':
                    print(f'\n{player_list[i].name} choose to STAND')
                    player_list[i].playing = False
                    break
                else:
                    pass


def show_some(player_list, dealer):

    print("\nShow current card.")
    print("\nDealer's card:\n   {}".format(dealer.cards[0]))
    for i in range(len(dealer.cards)-1):
        print('   <<<Hidden>>>')
    for i in range(player_num):
        print("\n{}'s card:".format(player_list[i].name))
        for card in player_list[i].cards:
            print(f'    {card}')
        print(
            f"{player_list[i].name}'s current value = {player_list[i].value}")


def show_all(player_list, dealer):

    print("\nShow all card.")
    print("\nDealer's card:")
    for card in dealer.cards:
        print(f'    {card}')
    for i in range(player_num):
        print("\nPlayer's card:")
        for card in player_list[i].cards:
            print(f'    {card}')


# following are the consequences that the game will get


def player_busts(player, dealer, player_chip):

    print(
        f"\n{player_name}' value is {player.value} and exceeds 21, the dealer wins.")
    print(f'{player_name} lost {player_chip.bet} bet.')
    player_chip.lose_bet()
    player.end = True


def player_wins(player, dealer, player_chip):

    print(
        f"\n{player.name}'s value is {player.value} and dealer's value is {dealer.value}, you win!")
    print(f'{player.name} got {player_chip.bet} bet.')
    player_chip.win_bet()
    player.end = True


def dealer_busts(player, dealer, player_chip):

    print(
        f"\nDealer's value is {dealer.value} and exceeds 21, {player.name} win!")
    print(f'{player.name} got {player_chip.bet} bet.')
    player_chip.win_bet()
    player.end = True


def dealer_wins(player, dealer, player_chip):

    print(
        f"\n{player.name}'s value is {player.value} and dealer's value is {dealer.value}, you lose.")
    print(f'{player.name} lost {player_chip.bet} bet.')
    player_chip.lose_bet()
    player.end = True


def push(player, dealer):

    print(
        f"\n{player.name}'s value is {player.value} and dealer's value is {dealer.value}, it's a push!")
    print(f"Nothing change for {player.name}'s' chips.")
    player.end = True


# Main Code

playing = True
play_round = 0
player_created = 0

while True:

    play_round += 1

    # Set up deck, players and dealer
    # Fisrt round and other round should be set up seperately
    if play_round == 1:
        print('Welcome to the BLACKJACK GAME!\n')
        while True:
            try:
                player_num = int(
                    input('How many players are joining this game? '))
            except:
                print('Invalid input, please type in positive integer.')
                continue
            else:
                if player_num <= 0:
                    print('Invalid input, number of player should be larger than 0.')
                    continue
                else:
                    break

        # Create & shuffle the deck, deal two cards to each player
        player_list = []
        dealer = Player('Dealer')
        for i in range(player_num):
            player_created += 1
            player_name = input(
                f'Please enter your name or press enter to use Player {player_created} as default name:')
            if player_name == '':
                player_list.append(Player(f'Player {player_created}'))
            else:
                player_list.append(Player(player_name))

        # Set up the deck
        deck = Deck()

    # reset data, re-create dealer and players(with same name)
    else:
        print('\nOne more game!')
        dealer = Player('Dealer')
        for i in range(player_num):
            name = player_list[i].name
            player_list[i] = Player(name)

    # Shuffle the deck and give two cards to each person
    deck.shuffle()
    for i in range(2):
        dealer.add_card(deck.deal())
        for j in range(len(player_list)):
            player_list[j].add_card(deck.deal())

    # Set up the Player's chips
    if play_round == 1:
        player_chip_list = []
        for i in range(player_num):
            player_chip_list.append(Chips())

    # Prompt the Player for their bet
    take_bet(player_list, player_chip_list)

    # Show cards (but keep one dealer card hidden)
    show_some(player_list, dealer)

    while playing:

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_list)

        # Show cards (but keep one dealer card hidden)
        show_some(player_list, dealer)

        # If player's hand exceeds 21, run player_busts() and change the player to 'not playing'
        for i in range(player_num):
            if player_list[i].adjust_for_ace() > 21:
                player_busts(player_list[i], dealer, player_chip_list[i])
                player_list[i].playing = False

        # Decide whether the game is end or not
        playing = False
        for i in range(player_num):

            # if anyone is still playing,then playing = True, game continue
            if player_list[i].playing:
                playing = True
            else:
                pass

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while dealer.value < 17:
        dealer.add_card(deck.deal())
        print("Dealer's value is smaller 17, draw one more card.")

    # Show all cards
    show_all(player_list, dealer)

    # Run different winning scenarios
    for i in range(player_num):
        if not player_list[i].end:
            if dealer.value > 21:
                dealer_busts(player_list[i], dealer, player_chip_list[i])
            elif player_list[i].value > dealer.value:
                player_wins(player_list[i], dealer, player_chip_list[i])
            elif player_list[i].value < dealer.value:
                dealer_wins(player_list[i], dealer, player_chip_list[i])
            elif player_list[i].value == dealer.value:
                push(player_list[i], dealer)
            else:
                pass

    # Inform Player of their chips total
    for i in range(player_num):
        print(
            f'{player_list[i].name} has {player_chip_list[i].total} chips now.')

    # Ask to play again
    reply = ''
    for i in range(player_num):
        while True:

            if player_chip_list[i].total == 0:
                print(f"{player_list[i].name}, you don't have any chip now")
                player_num -= 1
                player_list[i] = []
                player_chip_list[i] = []
                break
            reply = input(
                f'{player_list[i].name} play one more round or not? (y/n)').lower()
            if reply == 'y':
                break
            elif reply == 'n':
                print(
                    f'{player_list[i].name}, thanks for your playing and see you next time!')
                player_num -= 1
                player_list[i] = []
                player_chip_list[i] = []
                break
            else:
                print('Invalid input, please try again.')
    while [] in player_list:
        player_list.remove([])
        player_chip_list.remove([])

    if player_num != 0:
        playing = True
    else:
        break
