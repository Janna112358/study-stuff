def f(aap, kip):
    a = aap[0]
    b = aap[1]
    c = kip[0]
    d = kip[1]
    if a == b:
        if c == d:
            return [1]
        elif c != d:
            return [c, d]

    elif a != b:
        if c == d:
            return [a, b]
        elif c != d:
            if a == c and b == d:
                return [1]
            elif a == d and c == b:
                return [1]
            elif c == a:
                return [a, d, b]
            elif c == b:
                return [a, b, d]
            elif d == a:
                return [a, c, b]
            elif d == b:
                return [a, b, c]
            else:
                return ([a, b], [c, d])

def g(aap, kip):
    # aap = [a, b, ...]  # kip = [c, d, ...]
    z = aap + kip
    disjoint = True
    for a in z:
        if z.count(a) > 1:
            disjoint = False
    if disjoint:
        return ([aap, kip])
    
    s = []
    for i in range(len(aap) - 1):
        s.append([aap[i], aap[i+1]])
    for j in range(len(kip) - 1):
        s.append([kip[j], kip[j + 1]])]

    

    
