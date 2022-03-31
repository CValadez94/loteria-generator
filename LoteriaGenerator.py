import logging
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import shutil

import cv2 as cv


class LoteriaGenerator(object):
    def __init__(self, cc_count, gc_count, gc_cols, gc_rows):
        self._cc_count = cc_count
        self._gc_count = gc_count
        self._gc_cols = gc_cols
        self._gc_rows = gc_rows
        self._k = gc_cols * gc_rows
        self._PIC_DIR = os.getcwd() + '/pics'
        self._cc_images = []
        self._gc_templ_images = []
        self._game_card_sets = []

    def __get_images(self):
        cc_path = self._PIC_DIR + '/input/calling_cards'
        gc_templ_path = self._PIC_DIR + '/input/game_card_templates'
        cc_f_paths = [n for n in os.listdir(cc_path) if os.path.isfile(os.path.join(cc_path, n))]
        gc_templ_f_paths = [n for n in os.listdir(gc_templ_path) if os.path.isfile(os.path.join(gc_templ_path, n))]

        # Do some sanity checks first
        if len(cc_f_paths) != self._cc_count:
            print("You said there are {} calling card(s), but I only see {} image(s)..\n"
                  "Unfortunately I can't make that work. Aborting."
                  .format(self._cc_count, len(cc_f_paths)))
            return False

        if len(gc_templ_f_paths) < self._gc_count:
            print("You said you wanted {} game cards, but I only see {} game card template image(s)..\n"
                  "Unfortunately I can't make that work. Aborting."
                  .format(self._gc_count, len(gc_templ_f_paths)))
            return False

        print("Getting images...")
        cc_f_paths.sort()
        for f in cc_f_paths:
            self._cc_images.append(cv.imread(os.path.join(cc_path, f)))
        print("Got {:d} calling card images".format(len(self._cc_images)))

        gc_templ_f_paths.sort()
        for f in gc_templ_f_paths:
            self._gc_templ_images.append(cv.imread(os.path.join(gc_templ_path, f)))
        print("Got {:d} game card template images".format(len(self._gc_templ_images)))
        return True

    def __create_game_card_image(self, card_number, card_set, gc_insert_f_path, gc_f_path):
        # Create the game card insert image
        h = []
        v = []
        for i in range(self._gc_cols):
            for j in range(self._gc_rows):
                h.append(self._cc_images[card_set[i * self._gc_cols + j] - 1])
            v.append(np.hstack(h))
            h.clear()
        img_gc_insert = np.vstack(v)
        cv.imwrite(gc_insert_f_path, img_gc_insert)

        # Now insert the image inside the game card template image
        desired_width = 1237
        x_offset = 154
        y_offset = 182

        new_insert_dim = (desired_width, int((desired_width / img_gc_insert.shape[1]) * img_gc_insert.shape[0]))
        insert_resized = cv.resize(img_gc_insert, new_insert_dim, interpolation=cv.INTER_AREA)
        img_gc = self._gc_templ_images[card_number]
        img_gc[y_offset:y_offset + insert_resized.shape[0], x_offset:x_offset + insert_resized.shape[1]] \
            = insert_resized
        cv.imwrite(gc_f_path, img_gc)

    def __assemble(self):
        """Assemble everything
            - Create the game card insert images.
            - Put the game card insert images inside the game card template images
            - Create the calling card sheets
        """

        # Get the directories ready
        self.__verify_output_directory(self._PIC_DIR + '/output')
        gc_insert_out_dir = self._PIC_DIR + '/output/game_card_inserts'
        gc_out_dir = self._PIC_DIR + '/output/game_cards'
        cc_sheets_out_dir = self._PIC_DIR + '/output/calling_card_sheets'
        os.makedirs(gc_insert_out_dir)
        os.makedirs(gc_out_dir)
        os.makedirs(cc_sheets_out_dir)

        # Assemble the game cards
        for i in range(self._gc_count):
            print("  *Creating game card {}".format(i + 1))
            gc_insert_f_path = gc_insert_out_dir + '/game_card_insert_' + str(i + 1) + ".png"

            # Append a 0 if index less than 9
            if i < 9:
                gc_number = "0" + str(i + 1)
            else:
                gc_number = str(i + 1)

            gc_f_path = gc_out_dir + '/game_card_' + gc_number + ".png"
            self.__create_game_card_image(i, self._game_card_sets[i], gc_insert_f_path, gc_f_path)

        print("Created {} game cards at {}\n".format(self._gc_count, gc_out_dir))

        # Create the calling card sheets
        self.__create_calling_card_sheet_images(cc_sheets_out_dir)

    def create_game_cards(self):
        # Sanity check
        if self._gc_cols < 2 or self._gc_rows < 2:
            print("Need at least 2 columns and rows! Aborting...")
            return

        # Get the images of the calling cards and game card templates
        if not self.__get_images():
            return

        # Create a random unique sample set for each game card until user satisfied with the statistics
        while True:
            game_card_sets_sorted = []
            for i in range(self._gc_count):
                while True:
                    s = random.sample(range(1, self._cc_count + 1), self._k)
                    s_sorted = sorted(s)
                    if game_card_sets_sorted.count(s_sorted):
                        print("Game card {} is a duplicate, creating a new one..".format(i))
                    else:
                        # print("card {}: {}".format(i, s))
                        self._game_card_sets.append(s)
                        game_card_sets_sorted.append(s_sorted)
                        break  # Created a unique game card

            # Print stats and ask user if they are ok to proceed. If not, recreate the game cards
            confirmation = self.__confirm_stats()
            if confirmation == 'y':
                print("Creating game cards, please wait..")
                plt.close('all')
                self.__assemble()
                # self.create_report()
                break
            elif confirmation == 'q':
                print("Aborting..")
                plt.close('all')
                break
            elif confirmation == 'n':
                print("Recreating the game cards..")
                self._game_card_sets.clear()  # Clear the list
            else:
                print("Don't know what you mean, will assume you meant no.")
                self._game_card_sets.clear()  # Clear the list

    def __confirm_stats(self):
        """Display some statistics of generated game cards and confirm ok with user to proceed"""

        # Setup the pyplot stuff first
        plt.clf()
        plt.xlabel("Calling Card")
        plt.ylabel("Occurrences")
        plt.grid()
        plt.ion()
        plt.show()
        plt.title("Total times a calling card shows up out of {} game cards".format(self._gc_count))

        occurrence = np.empty(self._cc_count, dtype=int)
        game_card_sets_flat = sum(self._game_card_sets, [])  # Flatten array
        for i in range(self._cc_count):
            # print("found i={} {} times".format(i+1, data_flat.count(i+1)))
            occurrence[i] = game_card_sets_flat.count(i + 1)

        # Check if a calling card is not used at all
        occurrence_list = np.ndarray.tolist(occurrence)
        if occurrence_list.count(0) > 0:
            print("  There was/were {} calling cards that are not used in any game card.".
                  format(occurrence_list.count(0)))
        else:
            print("  All calling cards were used at least once.")
        _min = occurrence.min()
        _max = occurrence.max()
        print("  Calling card occurrences min/max for {} game cards:"
              "\n   MIN: {} calling card(s) occurred {} time(s)"
              "\n   MAX: {} calling card(s) occurred {} time(s)".
              format(self._gc_count, occurrence_list.count(_min), _min, occurrence_list.count(_max), _max))

        plt.bar(range(1, self._cc_count + 1), occurrence)
        plt.pause(0.5)

        confirmation = input("\nOk to proceed? y=yes, n=no, q=quit: ")
        return confirmation

    def __create_calling_card_sheet_images(self, out_dir):
        """Create 3x3 calling card sheets with calling cards in numerical order"""

        # Goal is sheets of 3x3, check if padding is needed to reshape array
        num_sheets = int(np.ceil(self._cc_count / 9))
        num_images_to_pad = self._cc_count % 9
        pad = self._cc_images[0]
        calling_cards = self._cc_images

        # Pad image list with blank image so that it is divisible by 9
        for i in range(num_images_to_pad):
            calling_cards.append(pad)

        # Create the collages
        for s in range(num_sheets):
            print("  *Creating calling card sheet {}".format(s + 1))
            h = []
            v = []
            for i in range(3):
                for j in range(3):
                    h.append(self._cc_images[s * 9 + i * 3 + j])
                v.append(np.hstack(h))
                h.clear()

            img = np.vstack(v)

            # Now resize the image and paste into a white background image to add margins
            margin = 45
            blank_width = 1545
            blank_height = 2000
            img_margin = np.full([blank_height, blank_width, 3], 255)
            desired_width = blank_width - 2 * margin
            desired_height = int((desired_width / img.shape[1]) * img.shape[0])
            img_resized = cv.resize(img, (desired_width, desired_height), interpolation=cv.INTER_AREA)
            y_offset = int((img_margin.shape[0] - img_resized.shape[0]) / 2)
            img_margin[y_offset:y_offset + img_resized.shape[0], margin:margin + img_resized.shape[1]] \
                = img_resized

            # Append 0 if index less than 9
            if s < 9:
                gc_number = "0" + str(s + 1)
            else:
                gc_number = str(s + 1)

            # cv.imwrite(out_dir + "/calling_card_sheet_" + gc_number + ".png", img)
            cv.imwrite(out_dir + "/calling_card_sheet_" + gc_number + ".png", img_margin)
        print("Created {} calling card sheets at {}".format(num_sheets, out_dir))

    def __create_report(self):
        # Create a text report in the output folder to show what the algorithm
        # generated for each game card
        lines = []
        for i in range(self._gc_count):
            s = 'Card {}: '.format(i + 1)
            for j in range(self._k):
                s += str(self._game_card_sets[i][j]) + ' '
            s += '\n'
            lines.append(s)

        _path = self._PIC_DIR + '/output/report.txt'
        _file = open(_path, 'w')
        _file.writelines(lines)
        _file.close()

    def __verify_output_directory(self, out_dir):
        """Verify the output directory
            If it doesn't, create it.
            If it does, check if emtpy and warn user to move the files since they will be deleted
            """
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)  # Create directory if it does not exist
        else:
            if len(os.listdir(out_dir)) > 0:  # Directory exists and is not empty
                print("[WARNING] There are some files already generated in {}."
                      " Please move them since they will be deleted".
                      format(out_dir))
                if input("When ready press enter: ") == 'q':
                    print("Aborting..")
                    return
                else:  # Delete directory and contents
                    try:
                        shutil.rmtree(out_dir)
                    except OSError as e:
                        print("Error: %s : %s" % (out_dir, e.strerror))
                    os.mkdir(out_dir)  # shutil.rmtree() also deletes directory, so recreate it
