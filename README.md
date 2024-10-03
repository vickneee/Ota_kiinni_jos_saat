# Ota kiinni jos saat!

------------

## Sisällysluettelo
  1. [Projektin yleiskuvaus](#projektin-yleiskuvaus)
  2. [Ominaisuudet](#Ominaisuudet)
  3. [Tekniset tiedot](#Tekniset-tiedot)
  4. [Ryhmän jäsenet](#Ryhmän-jäsenet)

------------

### Projektin yleiskuvaus

Tämä projekti kehitettiin osana ryhmätyötä Ohjelmisto 1 -kurssilla Metropolia Ammattikorkeakoulussa.

Pelin idea pohjautuu Scotland Yard -lautapeliin. Pelissä kaksi etsivää jahtaa ympäristörikollista ympäri Euroopan lentokenttiä tavoitteenaan saada hänet kiinni ennen ajan loppumista. Rikollisen liikkeet näkyvät etsiville vain satunnaisesti, mutta johtolankoja seuraamalla hänet voi jäljittää. Pelaajat liikkuvat eri lentokenttien välillä käyttämällä eri kokoisia lentokoneita ja lentolippuja.

------------

### Ominaisuudet
#### Peli:
- Peli tukee 1-3 pelaajaa, jolloin pelaajat voivat toimia joko rikollisena tai etsivänä.
- Yksinpelissä pelaaja voi valita roolin ja pelata tietokonetta vastaan.
- Kahden pelaajan tilassa toinen pelaaja ohjaa molempia etsiviä.
#### Eri kokoiset lentokoneet ja lentoliput:
- Pelaajilla on käytössä erilaisia lentolippuja, jotka rajoittavat tai mahdollistavat liikkumisen eri etäisyyksillä:
    - Potkurikone: Lähimmät kaksi lentokenttää.
    - Matkustahakone: Lähimmistä kahdesta kaksi seuraavaa lentokenttää.
    - Yksityiskone: Kaksi kauimmaista lentokenttää.
#### Kätketyt liikkeet ja johtolankojen seuraaminen:
- Rikollisen edellinen olinpaikka ja käytetty lentolippu paljastetaan etsiville kierroksilla (1, 4, 7 ja 10).
- Rikolliset näkevät joka vuorolla, mistä etsivät ovat liikkuneet ja mitä lentolippua on käytetty.
#### Pelimekaniikka:
- Jokaisella vuorolla rikollisen siirrot piilotetaan etsiviltä konsolin tyhjentämisen avulla.
#### Poikkeavien suorituspolkujen hallinta:
- Pelissä on sisäänrakennettuja virheilmoituksia, jotka käsittelevät virheelliset syötteet, kuten:
    - Liian pitkä nimimerkki.
    - Käytössä oleva tai tyhjä nimimerkki.
    - Virheellinen lentokenttävalinta.

------------
  
### Tekniset tiedot.
- Peli on toteutettu Python kielellä.
- Pelissä hyödynnetään MariaDB-tietokantaa.
- Pythonin ja MariaDB välinen yhteys perustuu SQL-kyselyihin.
- Peli on pelattavissa konsolissa.

#### Tietokantataulut:
- airport 
- country
- game
- game_player
- past_movement
- player
- tickets

![Tietokanta](https://github.com/user-attachments/assets/5d0ca8c2-7ff7-439c-b886-d3c23762cf33)
  
------------

### Ryhmän jäsenet

| Nimet              |
|--------------------|
| Samu Kirjonen      |
| Alessa Pentinmikko |
| Doni Trivedi       |
| Victoria Vavulina  |
