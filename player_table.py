# Player 1, choose your role: (0 or 1)
def player_choose_the_role():
    try:
        role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))
        if role_type == 0:
            print("Olet valinnut rikollisen.")
            return role_type
        elif role_type == 1:
            print("Olet valinnut etsijän.")
            return role_type
        else:
            print("Virheellinen syöte. Ole hyvä ja syötä 0 rikolliselle tai 1 etsijälle.")
            role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))
    except ValueError:
        role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))
    return role_type


# How many players will be playing the game?
def how_many_players():
    print("Kuinka monta pelaajaa pelaa peliä?\n"
          "Jos vastaus on 1:\n"
          "Pelaaja pelaa tietokonetta vastaan ja pelaajan täytyy valita rooli.\n"
          "Jos vastaus on 2: \n"
          "Ensimmäinen pelaaja pelaa rikollista ja toinen pelaaja pelaa kahta etsijää.\n"
          "Jos vastaus on 3: \n"
          "Ensimmäinen pelaaja pelaa rikollista, toinen pelaaja pelaa etsijää ja kolmas pelaaja pelaa etsijää.")
    try:
        num_players = int(input("Syötä numero 1:n ja 3:n väliltä: "))
        if num_players == 1:
            print("Pelaaja pelaa tietokonetta vastaan.")
            player_choose_the_role()
            return num_players

        elif num_players == 2:
            return num_players
        elif num_players == 3:
            return num_players
        else:
            print("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä:")
            how_many_players()
    except ValueError:
        num_players = int(input("Syötä numero 1:n ja 3:n väliltä: "))
    return num_players


how_many_players()
