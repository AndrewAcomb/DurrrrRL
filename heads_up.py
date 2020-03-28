import sys, getopt
import game

def main(argv):
    if argv:

        print("Options besides human vs random with default settings coming soon.")
        exit()


    else:
        
        newgame = game.Game('human', 'random')
        newgame.play_game()


if __name__ == "__main__":
    main(sys.argv[1:])
