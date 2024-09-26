# Player 1, choose your role: (0 or 1)
def player_choose_the_role():
    try:
        role_type = int(input("Enter 0 for criminal or 1 for searcher: "))
        if role_type == 0:
            print("You have chosen criminal.")
            return role_type
        elif role_type == 1:
            print("You have chosen searcher.")
            return role_type
        else:
            print("Invalid input. Please enter 0 for criminal or 1 for searcher.")
            role_type = int(input("Enter 0 for criminal or 1 for searcher: "))
    except ValueError:
        role_type = int(input("Enter 0 for criminal or 1 for searcher: "))
    return role_type


# How many players will be playing the game?
def how_many_players():
    print("How many players will be playing the game?\n"
          "If the answer is 1.\n"
          "The player will be playing opposite the computer and player have to choose the role.\n"
          "If the answer is 2. \n"
          "The first player will be playing criminal and the second player will be playing 2 "
          "searchers.\n"
          "If the answer is 3. \n"
          "The first player will be playing criminal, the second player will be playing searcher\n"
          "and the third player will be playing searcher.")
    try:
        num_players = int(input("Enter a number between 1 and 3: "))
        if num_players == 1:
            print("The player will be playing opposite the computer. Now choose your role: (0 or 1)")
            player_choose_the_role()
            return num_players

        elif num_players == 2:
            return num_players
        elif num_players == 3:
            return num_players
        else:
            print("Invalid input. Please enter a number between 1 and 3.")
            how_many_players()
    except ValueError:
        num_players = int(input("Enter a number between 1 and 3: "))
    return num_players


how_many_players()
