def samenvoegen(L1, L2):
    resultaat = []
    lengte = min(len(L1), len(L2))
    for i in range(lengte):
        resultaat.append(L1[i])
        resultaat.append(L2[i])
    return resultaat

def weven(L1, L2):
    resultaat = []
    lengte = max(len(L1), len(L2))

    for i in range(lengte):
        resultaat.append(L1[i % len(L1)])
        resultaat.append(L2[i % len(L2)])
    return resultaat

def ritsen(L1, L2):
    resultaat = []
    kortste = min(len(L1), len(L2))
    for i in range(kortste):
        resultaat.append(L1[i])
        resultaat.append(L2[i])
    if len(L1) > len(L2):
        resultaat.extend(L1[kortste:])
    elif len(L1) < len(L2):
        resultaat.extend(L2[kortste:])
    return resultaat