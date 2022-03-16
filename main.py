import os
import random
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

PIC_DIR = os.getcwd() + '/pics/'


def get_images():
    print("Getting images...")
    _images = []
    _f_paths = [n for n in os.listdir(PIC_DIR) if os.path.isfile(os.path.join(PIC_DIR, n))]
    _f_paths.sort()
    for f in _f_paths:
        _images.append(cv.imread(os.path.join(PIC_DIR, f)))
    print("Got {:d} images".format(len(_images)))

    return _images


def create_collage(_img, p1, p2, p3, p4, _name):
    h1 = np.hstack([_img[p1 - 1], _img[p2 - 1]])
    h2 = np.hstack([_img[p3 - 1], _img[p4 - 1]])
    v = np.vstack([h1, h2])
    cv.imwrite(PIC_DIR + _name + ".jpeg", v)
    print("Created {:s}".format(_name))


# r: Number of calling cards
# k: Number of tiles per game card
# g: Number of game cards
def create_random_set(r, k, g):
    game_cards = []
    game_cards_sorted = []

    for i in range(g):
        while True:
            s = random.sample(range(1, r + 1), k)
            s_sorted = sorted(s)
            if game_cards_sorted.count(s_sorted):
                print("Found a duplicate for card {}".format(i))
            else:
                # print("card {}: {}".format(i, s))
                game_cards.append(s)
                game_cards_sorted.append(s_sorted)
                break  # Created a unique game card
    return game_cards


# data: The gaming cards
# r: Number of calling cards
def print_stats(data, r):
    b = np.empty(r, dtype=int)
    l = len(data)
    data_flat = sum(data, [])
    for i in range(r):
        # print("found i={} {} times".format(i+1, data_flat.count(i+1)))
        b[i] = data_flat.count(i + 1)

    # Check if a calling card is not used at all
    b_list = np.ndarray.tolist(b)
    if b_list.count(0) > 0:
        print("There was/were {} calling cards that are not used in any game card.".format(b_list.count(0)))
    min = b.min()
    max = b.max()
    print("Calling card occurences min/max for {} game cards:\n   MIN: {} calling card(s) occured only {} time(s)"
          "\n   MAX: {} calling card(s) occurred {} time(s)".
          format(l, b_list.count(min), min, b_list.count(max), max))

    plt.bar(range(1, r + 1), b)
    plt.xlabel("Calling Card")
    plt.ylabel("Occurences")
    plt.title("Total times a calling card shows up out of {} game cards".format(l))
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # Get images
    # images = get_images()

    r = 52  # Number of calling cards
    k = 16  # Number of tiles per game card
    g = 15  # Number of game cards to create

    # Create random and unique game cards
    card_sets = create_random_set(r, k, g)
    # print("\nSets: {}".format(card_sets))

    # Get some statistics
    print_stats(card_sets, r)

    # create_collage(images, 1, 2, 3, 4, "C1")
    print("Created {} game cards.".format(len(card_sets)))
