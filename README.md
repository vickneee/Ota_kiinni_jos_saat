# Ota kiinni jos saat!

Tämä projekti kehitettiin osana ryhmätyötä Ohjelmisto 1 -kurssilla Metropolia Ammattikorkeakoulussa.

------------

### Sisällysluettelo
  1. [Projektin yleiskuvaus](#projektin-yleiskuvaus)
  2. [Ominaisuudet](#Ominaisuudet)
  3. [Tekniset tiedot](#Tekniset-tiedot)
  4. [Ryhmän jäsenet](#Ryhmän-jäsenet)

------------

### Projektin yleiskuvaus

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
    - Matkustajakone: Lähimmistä kahdesta kaksi seuraavaa lentokenttää.
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
  
### Tekniset tiedot
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


![image](https://github.com/user-attachments/assets/3dd3e582-a5d8-4168-b76e-5bfc8c932a52)

![Image1](https://github.com/user-attachments/assets/58f9ab12-4660-4114-9e49-04d7c83c9810)

#### Konsolipelin kuvia:

<img width="1187" alt="Screenshot 2024-10-09 at 1 52 38" src="https://github.com/user-attachments/assets/cd1e155a-07fe-42b4-ad87-a130368565ba">
<img width="1182" alt="Screenshot 2024-10-09 at 1 53 22" src="https://github.com/user-attachments/assets/2fdabdf1-9f78-414f-8525-0dd1a687f665">
<img width="1182" alt="Screenshot 2024-10-09 at 1 53 53" src="https://github.com/user-attachments/assets/d38b4128-a051-40f0-bf05-a6ee055b71aa">

------------

### Ryhmän jäsenet

| Nimet              |
|--------------------|
| Samu Kirjonen      |
| Alessa Pentinmikko |
| Doni Trivedi       |
| Victoria Vavulina  |
