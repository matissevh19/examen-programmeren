def faculteit(n):
    if n == 0:
        return 1
    else:
        return n * faculteit(n-1)

aantal = int(input())
for i in range(aantal):
    n = int(input())
    if n > 13:
        print("invoer te groot")
    else:
        print(faculteit(n))