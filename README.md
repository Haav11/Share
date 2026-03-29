# Share

Ideana on, että käyttäjä pystyy tekemään ilmoituksen valmistamastaan ruoasta ja kutsumaan muita jakamaan ruoan hänen kanssaan. Nyt kun lähiaikoina on ollut puhetta ruoan riittämättömyydestä ruokajonoissa, niin sovelluksen avulla auttaminen mahdollistetaan matalalla kynnyksellä peruskansalaisille. Vaihtoehtoisesti käyttäjä voi pysyä yksityisenä ja jakaa ruokaa vain kavereidensa kesken.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ruokailmoituksia.
- Käyttäjä näkee sovellukseen lisätyt ruokailmoitukset.
- Käyttäjä pystyy etsimään ruokailmoituksia hakusanalla tai muulla perusteella.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjästä tilastoja ja käyttäjän lisäämät aktiiviset ruokailmoitukset.
- Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun (Esim. Vegaani, maidoton, fodmap, kasvisruoka yms). 
- Käyttäjä pystyy ilmoittautua osaksi ruoan jakoa.

Ohjeet sovelluksen käynnistämiseen:
Saat käynnistettyä sovelluksen omalla koneellasi terminaalin kautta lataamalla kloonin sovelluksesta ja siirtymällä sen kansioon.
- git clone [url]
- cd [kansion-nimi]
  
Kansiossa sinun tulee luoda ja siirtyä virtuaaliympäristöön komennoilla
- python3 -m venv venv 
- source venv/bin/activate
  
Lataa tarvittaessa tarvittavat kirjastot
- pip install flask [muut-kirjastot]
  
Suorita tämän jälkeen komento
- flask run
  
Avaa tämän jälkeen sovellus selaimessa.
