

def percent(cf, ca):
    try:
        return round(float(cf) / (float(cf) + float(ca)) * 100.00, 2)
    except:
        return 0


def ratio(one, two):
    try:
        return round(float(one) / float(two) * 100.00, 2)
    except:
        return 0


def c_60(c, toi, games=1):
    try:
        return round(float(c) * (60 * games) / float(toi), 2)
    except:
        return 0
