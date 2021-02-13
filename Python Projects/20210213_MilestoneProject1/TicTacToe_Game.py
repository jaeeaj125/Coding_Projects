import time
import random
from os import system, name


def clear():
    if name == 'nt':
        _ = system('cls')


def display_board(board):
    display_type = {'1': ' ', '2': ' | ', '3': '---+---+---'}
    print(display_type['1']+board[7]+display_type['2'] +
          board[8]+display_type['2']+board[9]+display_type['1'])
    print(display_type['3'])
    print(display_type['1']+board[4]+display_type['2'] +
          board[5]+display_type['2']+board[6]+display_type['1'])
    print(display_type['3'])
    print(display_type['1']+board[1]+display_type['2'] +
          board[2]+display_type['2']+board[3]+display_type['1'])


def player_input():
    player_mark = False
    while not player_mark:
        player1_mark = input('Player1, please choose X or O (X/O):').upper()
        if player1_mark == 'X':
            player_mark = True
            player2_mark = 'O'
            print('Player1 will be X and player2 will be O!')
        elif player1_mark == 'O':
            player_mark = True
            player2_mark = 'X'
            print('Player1 will be O and player2 will be X!')
        else:
            print('Invalid input!')
    return player1_mark, player2_mark


def choose_first():
    return random.randint(1, 2)


def space_check(board, position):
    return board[position] == " "


def player_choice(board):
    choice = 'NOT YET'
    while not choice.isdigit():
        choice = input('Please choose a position (1~9): ')
        if not choice.isdigit():
            print('Invalid Input!')
        elif int(choice) not in range(1, 10):
            print('Position out of range, please choose another position!')
            choice = 'NOT YET'  # Keep the loop continuing
        elif not space_check(board, int(choice)):
            print('The position is already marked!')
            choice = 'NOT YET'  # Keep the loop continuing
        else:
            return int(choice)


def place_marker(board, marker, position):
    board[position] = marker
    return board


def full_board_check(board):
    return not " " in board


def win_check(board, mark):
    win_arr = [mark, mark, mark]
    if board[1:4] == win_arr or board[4:7] == win_arr or board[7:10] == win_arr:
        return True
    elif board[1:8:3] == win_arr or board[2:9:3] == win_arr or board[3:10:3] == win_arr:
        return True
    elif board[1:10:4] == win_arr or board[3:8:2] == win_arr:
        return True
    else:
        return False


def replay():
    ans = ''
    while ans != 'Y' and ans != 'N':
        ans = input('Do you want to play again? (Y/N)').upper()
        print(ans)
    if ans == 'Y':
        return True
    else:
        return False

# Main Code


print('Welcome to Tic Tac Toe!\n')
start = True
while start:

    # Game setting and introduction
    game_board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    sample_board = ['#', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    print('This is the sample gameboard, the numbers in the box represent the positions for putting marks in.\n')
    display_board(sample_board)
    print("\nLet's start the game with an empty gameboard.\n")
    display_board(game_board)
    print('\n')

    # Create player information for calling
    [player1_mark, player2_mark] = player_input()
    player_name = ['#', 'Player1', 'Player2']
    player_id = {'Player1': player1_mark, 'Player2': player2_mark}
    current = choose_first()  # variable for identifying who is the current player
    print('\n{} will go first!\n'.format(player_name[current]))

    # Start playing
    finish = False
    while not finish:
        game_board[player_choice(game_board)] = player_id[player_name[current]]
        display_board(game_board)
        if win_check(game_board, player_id[player_name[current]]):
            finish = True
            print(f"\nCongradulation! {player_name[current]} win the game!")
        elif full_board_check(game_board):
            finish = True
            print("\nThe game board is full.")
        else:
            if current == 1:
                current = 2
            else:
                current = 1
    if replay():
        clear()
        pass
    else:
        break

# The end of the game
clear()
print('\nThis is the end of the game, thanks for playing!\n')
time.sleep(2.0)
clear()
