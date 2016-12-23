from Reversi import Reversi
from ReversiPlayers import *


def get_player(message):

    while True:
        print "%s:" % message
        print "1) AI"
        print "2) Other"

        user_option = raw_input().strip().lower()

        if user_option == "1" or user_option == "ai":
            return AIReversiPlayer()

        elif user_option == "2" or user_option == "other":
            return ReversiPlayer()

        else:
            print "Invalid selection"


def get_board_size():

    while True:
        print "Please input the size of the board: "

        try:
            board_size = int(raw_input())

            if board_size < 4 or board_size % 2 != 0:
                print "Size must be greater than 4, and an even number"
                continue
            else:
                return board_size

        except:
            print "Board Size must be an integer!\n"


if __name__ == "__main__":

    print "***Welcome to Reversi!***"

    player_1 = get_player("Please select Player 1")
    player_2 = get_player("Please select Player 2")

    board_size = get_board_size()

    reversi = Reversi(size=board_size) 

    print reversi

    while True:

        player_1_move = player_1.get_move(reversi)
        reversi.make_move(player_1_move)

        print reversi

        player_2_move = player_2.get_move(reversi)
        reversi.make_move(player_2_move)

        print reversi

        if player_1_move == "pass" and player_2_move == "pass":
            print "GAME OVER!"
            break

    # Print winner
    print "Final Scores"
    scores = reversi.get_score()
    max_score = max(scores[0], scores[1])

    if max_score == scores[0]:
        print "Player 1 wins!!",
    elif max_score == scores[1]:
        print "Player 2 wins!!",
    else:
        print "It's a tie!",

    print "(%s - %s)" % (scores[0], scores[1])






