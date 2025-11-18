def iszigzag(reeks):
    for i in range(1, len(reeks)):
        if i % 2 == 1:
            if reeks[i] > reeks[i - 1]:
                return False
        else:
            if reeks[i] < reeks[i - 1]:
                return False
    return True

def zigzag_traag(reeks):
    reeks.sort()
    for i in range(0, len(reeks) - 1, 2):
        reeks[i], reeks[i + 1] = reeks[i + 1], reeks[i]

def zigzag_snel(reeks):
    for i in range(len(reeks) - 1):
        if i % 2 == 0:
            if reeks[i] < reeks[i + 1]:
                reeks[i], reeks[i + 1] = reeks[i + 1], reeks[i]
        else:
            if reeks[i] > reeks[i + 1]:
                reeks[i], reeks[i + 1] = reeks[i + 1], reeks[i]
