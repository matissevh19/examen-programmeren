numlist = [ 100, 101, 0, "103", 104 ]

try:
    i1 = int( input( "Give an index: " ) )
    print( "100 /", numlist[i1], "=", 100 / numlist[i1] )
except ValueError:
    print("Fout: geen geheel getal")
except IndexError:
    print("Fout: ongeldige index")
except ZeroDivisionError:
    print("Fout: kan niet delen door nul")
except TypeError:
    print("Fout: ongeldig type")