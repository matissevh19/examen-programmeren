def sorteer(rij):
    n = len(rij)
    stap = 1
    while stap < n:
        for i in range(0, n, 2 * stap):
            midden = i + stap
            einde = min(i + 2 * stap, n)
            links = rij[i:midden]
            rechts = rij[midden:einde]
            gemerged = merge(links, rechts)
            rij[i:einde] = gemerged
        stap *= 2


def merge(left, right):
    resultaat = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            resultaat.append(left[i])
            i += 1
        else:
            resultaat.append(right[j])
            j += 1
    resultaat.extend(left[i:])
    resultaat.extend(right[j:])
    return resultaat