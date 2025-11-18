def combisom(LGG: list, x: int):
    for i in range(len(LGG)):
        for j in range(len(LGG)):
            if i !=j and LGG[i] + LGG[j] == x:
                return True
    return False