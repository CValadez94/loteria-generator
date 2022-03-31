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


def get_specific_user_input(_question):
    """ Get valid user input for a specific question. Status = (0=no issues, 1=invalid input, 2=quit) """

    _result = 0
    _status = 0
    _retry_flag = True
    while _retry_flag:
        ans = input(_question)

        # Check for quit input
        if ans == 'q':
            _status = 1
            break

        # Check if input is non-zero integer
        if ans.isnumeric():
            ans_int = int(ans)
            if ans_int > 0:
                _result = ans_int
                _retry_flag = False
            else:
                print("\n**Please enter non-zero numeric characters only**\n")
        else:
            print("\n**Please enter numeric characters only**\n")

    return [_status, _result]


if __name__ == '__main__':
    """Get parameters from user and run the loteria card generator"""

    print("Welcome to the Lotería Card generator")
    print("Enter the following information:\n")

    status, cc_count, gc_count, gc_cols, gc_rows = get_user_input()
    if status == 1:  # Status 1 is quit flag
        exit()
    print("")

    # Create random and unique game cards
    lcg = LoteriaGenerator(cc_count, gc_count, gc_cols, gc_rows)
    lcg.create_game_cards()

    # Repeat using same calling cards, templates and parameters.
    # Only parameter that can change now is the number of game cards
    while True:
        print("= == = == = == = == = == = == = == = == = == = == = == = == = == = ==\n")
        if input("Press 'enter' if you want to generate again, press 'q' if you want to quit: ") == 'q':
            break
        print("")
        status, gc_count = get_specific_user_input("How many game cards do you need? ")
        if status == 1:  # Status 1 is quit flag
            break

        lcg.set_gc_count(gc_count)
        lcg.create_game_cards(reuse=True)
