def hanoi(n, start='A', hulp='B', eind='C'):
    stappen = []
    def verplaats(aantal, van_paal, via_paal, naar_paal):
        if aantal == 1:
            stappen.append(f"Schijf 1 van {van_paal} naar {naar_paal}")
        else:
            verplaats(aantal - 1, van_paal, naar_paal, via_paal)
            stappen.append(f"Schijf {aantal} van {van_paal} naar {naar_paal}")
            verplaats(aantal - 1, via_paal, van_paal, naar_paal)
    verplaats(n, start, hulp, eind)

    for stap in stappen:
        print(stap)

    print(f"{len(stappen)} stappen gedaan")