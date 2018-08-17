# Script:  energyair-bot.py
# Version: v2.0

# Imports
import sys
from lxml import html
import requests
import time

unanswered = dict()
errors = 0
wrong = 0
rounds = 0
schief = 0
phoneNumber = '0792963423'

# Questions and answers
questions = {
    'Was passiert, wenn es am Eventtag regnet?' : 2,
    'Was ist Cyrils (Aaron Hilmer) Markenzeichen im Film?' : 1,
    'Mit welchem dieser Tickets geniesst du die beste Sicht zur Energy Air Bühne?' : 0,
    'Welcher Schweizer Shootingstar spielt in DAS SCHÖNSTE MÄDCHEN DER WELT die Hauptrolle?' : 0,
    'Was ist Cyrils besondere Begabung?' : 0,
    'Die wievielte Energy Air Ausgabe findet dieses Jahr statt?' : 2,
    'Welcher Schauspieler/Rapper trägt im Film eine goldene Maske?' : 1,
    'Mit welchem Preis wurde der Nachwuchsstar Luna Wedler dieses Jahr ausgezeichnet?' : 0,
    'Wohin führt die Klassenfahrt?' : 2,
    'Wo findet das Energy Air statt?' : 0,
    'Wann fand Energy Air zum ersten Mal statt?' : 0,
    'Wo erfährst du immer die neusten Infos rund um Energy Air?' : 1,
    'Wer stand am letzten Energy Air als Überraschungsgast auf der Bühne?' : 0,
    'Welche Fussballmannschaft ist im Stade de Suisse zuhause?' : 2,
    'Wann ist der offizielle Filmstart von DAS SCHÖNSTE MÄDCHEN DER WELT in den Schweizer Kinos?' : 1,
    'Wie viele Acts waren beim letzten Energy Air dabei?' : 0,
    'Wer spielt die Mutter von Cyril?' : 2,
    'Wer eröffnete das erste Energy Air?' : 1,
    'Wann findet das Energy Air 2018 statt?' : 0,
    'Das NRJ-Gefährt ist ein…' : 1,
    'Wann beginnt das Energy Air 2018?' : 0,
    'Welcher dieser Acts hatte einen Auftritt am Energy Air 2017?' : 1,
    'Energy Air Tickets kann man…' : 0,
    'Energy Air ist der einzige Energy Event, …' : 0,
    'Wer war der letzte Act beim Energy Air 2017?' : 1,
    'Wie schwer ist die Energy Air Bühne?' : 0,
    'Welche Farbe haben die Haare des Social Media Stars Julia Beautx im Film?' : 0,
    'Wie viele Energy Air Tickets werden verlost?' : 2,
    'Wann ist offiziell Türöffnung beim Energy Air?' : 1,
    'Wie viele Sitzplätze hat das Stade de Suisse bei Sport Veranstaltungen?' : 1,
    'Wo kann man Energy Air Tickets kaufen?' : 3,
    'Zum wievielten Mal findet das Energy Air statt?' : 2,
    'Von welchem ehemaligen Energy Air Act ist der Song «Bilder im Kopf»?' : 1,
    'Welcher Act stand NOCH NIE auf der Energy Air Bühne?' : 3,
    'Wie hiess das Stade de Suisse früher?' : 1,
    'Wie viel kostet ein Energy Air Ticket?' : 1,
    'Welcher Act stand NOCH NIE auf der Energy Air Bühne?' : 1,
    'Welche Farben dominieren das Energy Air Logo?' : 3,
    'Welcher Act stand schon einmal auf der Energy Air Bühne?' : 1,
    'Wer war der letzte Act am Energy Air 2016?' : 3,
    'In welchen Schweizer Stadt hat Energy KEIN Radiostudio?' : 3,
    'Wann fand das erste Energy Air statt?' : 1,
    'Von welchem vergangenen Energy Air Act ist der Song «Angelina»?' : 1,
    'Wie viele Zuschauer passen ins Stade de Suisse?' : 1,
    'Wie hiess der Energy Air Song im Jahr 2014?' : 3,
    'Wie viele Tage dauert das Energy Air?' : 3,
    'Von wem wird das Energy Air durchgeführt?' : 1,
    'Wie viel kostet die Energy Air App?' : 2,
    'Wie viele Tickets werden für das Energy Air verlost?' : 1,
    'Wie gross ist die Spielfläche des Stade de Suisse?' : 2,
    'Wie hiess im Jahr 2015 die Energy Air Hymne?' : 1,
    'Das Energy Air ist ...?' : 1,
    'Wie viele Male standen Dabu Fantastic bereits auf der Energy Air Bühne?' : 1,
    'Welcher Fussballverein ist im Stade de Suisse Zuhause?' : 1,
    'Ab wann darf man am Energy Air teilnehmen?' : 1,
    'Was ist die obere Altersbeschränkung des Energy Air?' : 2,
    'In welchem Monat findet das Energy Air jeweils statt?' : 2,
    'Was für Plätze gibt es am Energy Air?' : 3,
    'In welcher Schweizer Stadt hat Energy KEIN Radiostudio?' : 3
}


def get_answer(question):
    print(question)
    answer = questions.get(question, 0)
    if answer == 0:
        print("unanswered")
        unanswered.update({question: 0})
        return 1
    return answer


def next_question(antwort):
    data = {'question': antwort}
    q2 = session.post('https://game.energy.ch/', data)
    tree = html.fromstring(q2.content)
    frage = tree.xpath('//form[@class="question"]/h1/text()')[0]
    return frage


try:
    while True:
        try:
            rounds += 1
            session = requests.session()
            data = {'mobile': phoneNumber}
            q1 = session.post('https://game.energy.ch/', data)
            tree = html.fromstring(q1.content)

            frage = tree.xpath('//form[@class="question"]/h1/text()')[0]

            for i in range(9):
                time.sleep(0.5)
                antwort = get_answer(frage)
                frage = next_question(antwort)
            antwort = get_answer(frage)

            data = {'question': antwort}
            q2 = session.post('https://game.energy.ch/', data)
            print("alles beantwortet")

            tree = html.fromstring(q2.content)
            verloren = tree.xpath('//div[@id="content"]/h2/text()')
            print(verloren)
            if verloren[0] == "Glückwunsch!":
                data = {'site': 'win'}
                q2 = session.post('https://game.energy.ch/', data)
                print("auf auswahl seite")
                q2 = session.get('https://game.energy.ch/?ticket=10')
                print("auf endseite")
                tree = html.fromstring(q2.content)
                verloren = tree.xpath('//div[@id="wingame"]/h1/text()')
                if len(verloren) == 1:
                    if verloren[0] != "Das war das falsche Logo, knapp daneben! Versuche es erneut!":
                        f = open('win.txt', 'wb')
                        f.write(q2.content)
                        f.close()
                        print("gewonnen!!??")
                    else:
                        print("verloren - restart")
                else:
                    print("Etwas ist schief gelaufen - restart")
                    schief += 1
            else:
                wrong += 1
                print("zu wenig richtig - restart")

        except Exception:
            print("Es gab ein Fehler - restart")
            errors += 1
            pass
finally:
    print("\n\n--FERTIG--")
    print("Anzahl Runden insgesamt: " + str(rounds))
    print("Anzahl Runden falsch beantwortet: " + str(wrong))
    print("Anzahl Fehler aufgetreten: " + str(errors))
    print("wubb wubb debug: " + str(schief))
    print("unanswered questions:")
    print(*unanswered.keys(), sep='\n')
    sys.exit(0)
