from game import Game

def main():
    game = Game(single=True)
    game.run()
    game.close()

if __name__ == "__main__":
    main()