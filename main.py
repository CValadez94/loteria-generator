from LoteriaGenerator import LoteriaGenerator


def get_user_input():
    """
    Get valid user input and return integers. Status = (0=no issues, 1=invalid input, 2=quit)
    Outputs = [Number of calling cards, Number of calling cards
               Number of columns per game card, Number of rows per game card]
    """

    questions = ["How many calling cards are there? ", "How many game cards do you need? ",
                 "How many columns per game card? ", "How many rows per game card? "]

    _result = [0, 0, 0, 0]
    _status = 0
    _retry_flag = True
    while _retry_flag:
        _retry_flag = False
        for idx in range(len(questions)):
            ans = input(questions[idx])

            # Check for quit input
            if ans == 'q':
                _status = 1
                break

            # Check if input is non-zero integer
            if ans.isnumeric():
                ans_int = int(ans)
                if ans_int > 0:
                    _result[idx] = ans_int
                else:
                    print("\n**Please enter non-zero numeric characters only**\n")
                    _retry_flag = True
                    break
            else:
                print("\n**Please enter numeric characters only**\n")
                _retry_flag = True
                break

    _result.insert(0, _status)
    return _result


if __name__ == '__main__':
    """Get parameters from user and run the loteria card generator"""
    print("Welcome to the Lotería Card generator")
    print("Enter the following information:\n")
    while True:
        status, cc_count, gc_count, gc_cols, gc_rows = get_user_input()
        if status == 1:  # Status 1 is quit flag
            break
        print("")
        lcg = LoteriaGenerator(cc_count, gc_count, gc_cols, gc_rows)

        # Create random and unique game cards
        lcg.create_game_cards()

        # Create the sheets of calling cards in numerical order
        # lcg.create_calling_card_sheets()

        print("= == = == = == = == = == = == = == = == = == = == = == = == = == = ==\n")
        if input("Press 'enter' if you want to generate again, press 'q' if you want to quit: ") == 'q':
            break
        print("")
