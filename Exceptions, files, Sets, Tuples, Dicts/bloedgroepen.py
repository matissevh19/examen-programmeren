def bloedgroep_kind(ouder1, ouder2):
    bloedgroepen = {
        "A": ["A", "O"],
        "B": ["B", "O"],
        "AB": ["A", "B"],
        "O": ["O"]
    }

    ABO_ouder1 = ouder1[:-1]
    ABO_ouder2 = ouder2[:-1]

    rhesus_ouder1 = ouder1[-1]
    rhesus_ouder2 = ouder2[-1]

    allelen_1 = bloedgroepen[ABO_ouder1]
    allelen_2 = bloedgroepen[ABO_ouder2]

    mogelijke_bloedgroepen = set()

    for allel1 in allelen_1:
        for allel2 in allelen_2:
            if (allel1 == "A" and allel2 == "B") or (allel1 == "B" and allel2 == "A"):
                mogelijke_bloedgroepen.add("AB")
            elif allel1 == allel2:
                mogelijke_bloedgroepen.add(allel1)
            else:
                if allel1 == "A" or allel2 == "A":
                    mogelijke_bloedgroepen.add("A")
                elif allel1 == "B" or allel2 == "B":
                    mogelijke_bloedgroepen.add( "B")

    mogelijke_rhesus = set()

    if rhesus_ouder1 == "+" or rhesus_ouder2 == "+":
        mogelijke_rhesus.add("+")
        mogelijke_rhesus.add("-")
    else:
        mogelijke_rhesus.add("-")

    resultaat = set()

    for bloedgroep in mogelijke_bloedgroepen:
        for rhesus in mogelijke_rhesus:
            resultaat.add(bloedgroep + rhesus)

    return resultaat

def bloedgroep_ouder(ouder, kind):
    mogelijke = set()
    for bg in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
        if kind in bloedgroep_kind(ouder, bg):
            mogelijke.add(bg)
    return mogelijke
