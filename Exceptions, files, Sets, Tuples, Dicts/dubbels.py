def dubbel(lijst):
    gezien = set()
    for getal in lijst:
        if getal in gezien:
            return getal
        gezien.add(getal)
    return None


def dubbels(lijst):
    een_keer = set()
    meer_keer = set()
    for getal in lijst:
        if getal in een_keer:
            een_keer.remove(getal)
            meer_keer.add(getal)
        elif getal not in meer_keer:
            een_keer.add(getal)
    return een_keer, meer_keer