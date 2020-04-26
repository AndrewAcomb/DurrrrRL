import sys, getopt, math, datetime
import game

def main(argv):
    if not argv:
        p1 = 'human'
        p2 = 'random'

    elif len(argv) == 1:
        p1 = 'human'
        p2 = argv[0]

    else:
        p1 = argv[0]
        p2 = argv[1]

    show_output = True if len(argv) > 2 else False

    # For interactive testing: python3 heads_up.py human agent
    # For initial training: python3 heads_up.py agent omniscient
    # For later training: python3 heads_up.py agent agent

    newgame = game.Game([p1, p2], show_output=show_output)
    newgame.play_game()



if __name__ == "__main__":
    main(sys.argv[1:])
