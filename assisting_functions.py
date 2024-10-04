import os
from math import radians, cos, sin, asin, sqrt
from playsound import playsound


# Play music when the game ends
def play_celebration_sound():
    playsound('assets/celebration.mp3')


# Clear console
def tyhj():
    os.system('cls' if os.name == 'nt' else 'clear')


# Game instructions
def game_instructions():
    print("Pelin ohjeet:\n")

    print("1. Pelaajamäärä:")
    print("   - Peliä voi pelata yksi, kaksi tai kolme pelaajaa.")
    print(
        "- Yhden pelaajan pelissä pelaaja saa päättää, että pelaako hän etsivän vai rikollisen roolia ja pelaa tietokonetta vastaan.")
    print("   - Kahden pelaajan pelissä toinen pelaajista ohjaa molempia etsiviä.\n")

    print("2. Roolit ja lentoliput:")
    print("   - Pelissä on kaksi etsivää. Heillä on per etsivä:")
    print("     * 5 potkurikoneen lentolippua")
    print("     * 3 matkustajakoneen lentolippua")
    print("     * 2 yksityiskoneen lentolippua")
    print("   - Pelissä on yksi rikollinen. Hänellä on:")
    print("     * 10 potkurikoneen lentolippua")
    print("     * 6 matkustajakoneen lentolippua")
    print("     * 4 yksityiskoneen lentolippua\n")

    print("3. Lentolippujen toiminta:")
    print("   - Potkurikoneella pääsee kahdelle lähimmälle lentokentälle.")
    print("   - Matkustajakoneella kahdelle siitä seuraavaksi lähimmille lentokentille.")
    print("   - Yksityiskoneella kahdelle kauimmaiselle lentokentälle.\n")

    print("4. Pelin kulku:")
    print("   - Pelissä on 21 ennalta määritettyä lentokenttää.")
    print("   - Etsivät eivät voi käyttää ensimmäisellä vuorolla yksityiskoneen lentolippua.")
    print("   - Rikollisen edellinen olinpaikka näytetään kierroksilla 1, 4, 7 ja 10.")
    print("   - Rikollinen näkee etsivien sijainnin joka vuorolla.")
    print("   - Peli alkaa rikollisen vuorolla.")
    print(
        "   - Peli päättyy kymmenen kierroksen jälkeen tai kunnes toinen etsivistä saa rikollisen kiinni menemällä samalle lentokentälle, jossa rikollinen on,")
    print("     tai rikollinen lentää samalle lentokentälle, jossa etsivä sijaitsee.")


# Calculate the distance between two geographical points using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


# Ascii art. And the end message
def thank_you():
    print("""
▄    ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄
▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌
▐░▌ ▐░▌  ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌
▐░▌▐░▌       ▐░▌          ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌          ▐░▌
▐░▌░▌        ▐░▌          ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌
▐░░▌         ▐░▌          ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌
▐░▌░▌        ▐░▌          ▐░▌          ▐░▌     ▐░▌       ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░▌
▐░▌▐░▌       ▐░▌          ▐░▌          ▐░▌     ▐░▌       ▐░▌          ▐░▌ ▀
▐░▌ ▐░▌  ▄▄▄▄█░█▄▄▄▄  ▄▄▄▄█░█▄▄▄▄      ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌ ▄
▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌
▀    ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀ 
    """)
    print("Kiitos kun pelasit lentokonepeliä!")
    print("Peli on kehitetty osana Ohjelmisto 1 -kurssia.")
    print("Koodin ovat kirjoittaneet: ")
    print("    - Samu Kirjonen")
    print("    - Alessa Pentinmikko")
    print("    - Doni Trivedi")
    print("    - Victoria Vavulina")
