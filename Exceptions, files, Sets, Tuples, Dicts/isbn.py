def overzicht(codes):
    groepen = {
        "Engelstalige landen": 0,
        "Franstalige landen": 0,
        "Duitstalige landen": 0,
        "Japan": 0,
        "Russischtalige landen": 0,
        "China": 0,
        "Overige landen": 0,
        "Fouten": 0
    }

    for code in codes:
        if not code.isdigit() or len(code) != 13:
            groepen["Fouten"] += 1
            continue

        if not (code.startswith("978") or code.startswith("979")):
            groepen["Fouten"] += 1
            continue

        cijfers = [int(c) for c in code]
        oneven = sum(cijfers[i] for i in range(0, 12, 2))
        even = sum(cijfers[i] for i in range(1, 12, 2))
        controle = (10 - (oneven + 3 * even) % 10) % 10

        if cijfers[-1] != controle:
            groepen["Fouten"] += 1
            continue

        vierde = code[3]
        if vierde in ("0", "1"):
            groepen["Engelstalige landen"] += 1
        elif vierde == "2":
            groepen["Franstalige landen"] += 1
        elif vierde == "3":
            groepen["Duitstalige landen"] += 1
        elif vierde == "4":
            groepen["Japan"] += 1
        elif vierde == "5":
            groepen["Russischtalige landen"] += 1
        elif vierde == "7":
            groepen["China"] += 1
        elif vierde in "689":
            groepen["Overige landen"] += 1
        else:
            groepen["Fouten"] += 1

    for groep in groepen:
        print(f"{groep}: {groepen[groep]}")
