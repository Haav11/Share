# Share

Ideana on, että käyttäjä pystyy tekemään ilmoituksen valmistamastaan ruoasta ja kutsumaan muita jakamaan ruoan hänen kanssaan. Nyt kun lähiaikoina on ollut puhetta ruoan riittämättömyydestä ruokajonoissa, niin sovelluksen avulla auttaminen mahdollistetaan matalalla kynnyksellä peruskansalaisille.

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ruokailmoituksia.
- Käyttäjä näkee sovellukseen lisätyt ruokailmoitukset.
- Käyttäjä pystyy etsimään ruokailmoituksia nimen tai ruokavalion perusteella.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjästä tilastoja ja käyttäjän lisäämät aktiiviset ruokailmoitukset.
- Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun (vegaaninen, gluteeniton, kasvis, laktoositon). 
- Käyttäjä pystyy ilmoittautumaan osaksi ruoan jakoa ja perumaan ilmoittautumisensa.


## Ohjeet sovelluksen käynnistämiseen

Saat käynnistettyä sovelluksen omalla koneellasi terminaalin kautta seuraavasti:

1. **Kloonaa repositorio ja siirry kansioon:**
   ```
   git clone [url]
   cd [kansion-nimi]
   ```

2. **Luo ja aktivoi virtuaaliympäristö:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Asenna `flask`-kirjasto:**
   ```
   pip install flask
   ```

4. **Luo tietokannan taulut ja lisää alkutiedot:**
   ```
   sqlite3 database.db < schema.sql
   sqlite3 database.db < init.sql
   ```

5. **Käynnistä sovellus:**
   ```bash
   flask run
   ```
   Avaa sovellus selaimessa
