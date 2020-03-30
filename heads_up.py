import sys, getopt
import game

def main(argv):
    if argv:

        newgame = game.Game('random', 'random', show_output=False)
        newgame.play_game()


    else:
        
        newgame = game.Game('human', 'random')
        newgame.play_game()


if __name__ == "__main__":
    main(sys.argv[1:])
