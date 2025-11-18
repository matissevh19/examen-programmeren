def mergesort(lst):
    if len(lst) <= 1:
        return lst
    midden = len(lst) // 2
    linkerhelft = mergesort(lst[:midden])
    rechterhelft = mergesort(lst[midden:])
    return merge(linkerhelft, rechterhelft)

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