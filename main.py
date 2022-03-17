import os
import random
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class LoteriaCardGenerator(object):
    # r: Number of calling cards
    # k: Number of tiles per game card
    # g: Number of game cards
    def __init__(self, _r, _cols, _rows, _g):
        self.r = _r
        self.cols = _cols
        self.rows = _rows
        self.k = _cols * _rows
        self.g = _g
        self.PIC_DIR = os.getcwd() + '/pics/'
        self.images = []
        self.game_card_sets = []

    def get_images(self):
        print("Getting images...")
        _cc_path = self.PIC_DIR + '/calling_cards'
        _f_paths = [n for n in os.listdir(_cc_path) if os.path.isfile(os.path.join(_cc_path, n))]

        # Do a sanity check first to make sure number of calling card pictures matches r
        if len(_f_paths) != self.r:
            print("You said there are {} calling cards, but I see {} images..\n"
                  "I can't work under these conditions! Aborting."
                  .format(self.r, len(_f_paths)))
            return False

        _f_paths.sort()
        for f in _f_paths:
            self.images.append(cv.imread(os.path.join(_cc_path, f)))
        print("Got {:d} images".format(len(self.images)))
        return True

    def create_collage(self, _set, _name):
        h = []
        v = []
        for i in range(self.cols):
            for j in range(self.rows):
                h.append(self.images[_set[i * self.cols + j] - 1])
            v.append(np.hstack(h))
            h.clear()

        img = np.vstack(v)
        cv.imwrite(self.PIC_DIR + '/output/' + _name + ".jpeg", img)

    def assemble_gaming_cards(self):
        for i in range(self.g):
            name = 'GC' + str(i + 1)
            print("  *Create game card {}".format(name))
            self.create_collage(self.game_card_sets[i], name)

    def create_game_cards(self):
        # Sanity check
        if self.cols < 2 or self.rows < 2:
            print("Is this a joke? Need at least 2 columns and rows! Aborting.")
            return

        # Get the images, abort if sanity check not passed
        if not self.get_images():
            return

        while True:
            game_card_sets_sorted = []
            for i in range(self.g):
                while True:
                    s = random.sample(range(1, self.r + 1), self.k)
                    s_sorted = sorted(s)
                    if game_card_sets_sorted.count(s_sorted):
                        print("Card {} was duplicate, creating new one..".format(i))
                    else:
                        # print("card {}: {}".format(i, s))
                        self.game_card_sets.append(s)
                        game_card_sets_sorted.append(s_sorted)
                        break  # Created a unique game card

            # Print stats and ask user if they are ok to proceed. If not, recreate the game cards
            self.print_stats()
            user_input = input("\nOk to proceed? y=yes, n=no, a=abort: ")
            if user_input == 'y':
                print("Creating game cards, please wait..")
                self.assemble_gaming_cards()
                self.create_report()
                print("Created {} game cards at {}".format(self.g, self.PIC_DIR + 'output'))
                break
            elif user_input == 'a':
                print("Aborting..")
                break
            elif user_input == 'n':
                print("Recreating the game cards..")
                plt.clf()
                self.game_card_sets.clear()  # Clear the list
            else:
                print("Don't know what you mean, will assume you meant no.")

    def print_stats(self):
        # Setup the pyplot stuff first
        plt.clf()
        plt.xlabel("Calling Card")
        plt.ylabel("Occurrences")
        plt.grid()
        plt.ion()
        plt.show()

        _b = np.empty(r, dtype=int)
        _l = len(self.game_card_sets)
        plt.title("Total times a calling card shows up out of {} game cards".format(_l))
        _data_flat = sum(self.game_card_sets, [])
        for i in range(r):
            # print("found i={} {} times".format(i+1, data_flat.count(i+1)))
            _b[i] = _data_flat.count(i + 1)

        # Check if a calling card is not used at all
        _b_list = np.ndarray.tolist(_b)
        if _b_list.count(0) > 0:
            print("  There was/were {} calling cards that are not used in any game card.".format(_b_list.count(0)))
        else:
            print("  All calling cards were used at least once.")
        _min = _b.min()
        _max = _b.max()
        print("  Calling card occurrences min/max for {} game cards:"
              "\n   MIN: {} calling card(s) occurred only {} time(s)"
              "\n   MAX: {} calling card(s) occurred {} time(s)".
              format(_l, _b_list.count(_min), _min, _b_list.count(_max), _max))

        plt.bar(range(1, r + 1), _b)
        plt.pause(0.5)

    # Create a text report in the output folder to show what the algorithm
    # generated for each game card
    def create_report(self):
        lines = []
        for i in range(self.g):
            s = 'Card {}: '.format(i + 1)
            for j in range(self.k):
                s += str(self.game_card_sets[i][j]) + ' '
            s += '\n'
            lines.append(s)

        _path = self.PIC_DIR + '/output/report.txt'
        _file = open(_path, 'w')
        _file.writelines(lines)
        _file.close()


if __name__ == '__main__':
    r = 54  # Number of calling cards
    cols = 4  # Number of columns  per game card
    rows = 4  # Number of rows per game card
    g = 30  # Number of game cards to create
    lcg = LoteriaCardGenerator(r, cols, rows, g)

    # Create random and unique game cards
    lcg.create_game_cards()
