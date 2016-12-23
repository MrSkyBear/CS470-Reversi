class AIReversiPlayer():
    def __init__(self):
        pass

    def get_move(self, reversi):
        return reversi.get_optimal_move()


class ReversiPlayer():
    def __init__(self):
        pass

    def get_move(self, reversi):

        while True:
            print "Enter your move (%s): " % reversi.current_player_turn.upper()

            player_move = raw_input().lower()
            if player_move != "pass":

                try:
                    player_move = [int(x) for x in player_move.replace(' ', '').split(',')]
                    player_move = (player_move[0], player_move[1])
                except:
                    print "Invalid move syntax"
                    continue


            if (reversi.move_is_valid(player_move)):
                return player_move
            else:
                print "Invalid Move!"





