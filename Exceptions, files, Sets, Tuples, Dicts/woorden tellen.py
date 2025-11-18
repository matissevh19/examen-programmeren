def woorden_splitsen(txt):
    file = open(txt, "r")
    inhoud = file.read()
    woorden = inhoud.split()
    gestript = []
    for woord in woorden:
        woordje = woord.strip('?.!,:;()')
        gestript.append(woordje)
    return gestript


def woorden_tellen(bestandsnaam):
    woorden = woorden_splitsen(bestandsnaam)
    telling = {}
    for w in woorden:
        w = w.lower()
        if w in telling:
            telling[w] += 1
        else:
            telling[w] = 1
    return telling
