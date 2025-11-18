def sorteer(lijst):
    quicksort(lijst, 0, len(lijst) - 1)


def quicksort(rij, laag, hoog):
    if laag < hoog:
        spil_index = verdeel(rij, laag, hoog)
        quicksort(rij, laag, spil_index - 1)
        quicksort(rij, spil_index + 1, hoog)


def verdeel(rij, laag, hoog):
    spil = rij[hoog]
    i = laag - 1
    for j in range(laag, hoog):
        if rij[j] <= spil:
            i += 1
            rij[i], rij[j] = rij[j], rij[i]
    rij[i + 1], rij[hoog] = rij[hoog], rij[i + 1]
    return i + 1

