def zoek(gesorteerd: list, x: int):
    low = 0
    high = len(gesorteerd) - 1

    while low <= high:
        mid = (low + high) // 2
        if gesorteerd[mid] == x:
            return mid
        elif gesorteerd[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return None
