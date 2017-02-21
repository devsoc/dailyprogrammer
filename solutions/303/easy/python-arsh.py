# /r/dailyprogrammer challenge 303 easy with bonus


def corner(x, y, h, w):
    if x == 0 and y == h:
        return 'LL'
    if x == w and y == 0:
        return 'UR'
    if x == w and y == h:
        return 'LR'
    return None


def check_corners(cords, h, w):
    if any(corner(*x, h, w) for x in cords) == False:
        return False
    else:
        return list(filter(None, [corner(*x, h, w) for x in cords]))[0]


def calc(h, w, m, n, v):
    xinc = yinc = 1
    bounce = steps = 0
    cords = [(0, 0), (n, 0), (n, m), (0, m)]

    while True:
        status = check_corners(cords, h, w)
        if status is not False:
            break

        cords = [(x + xinc, y + yinc) for x, y in cords]
        steps += 1
        if cords[0][0] == 0 or cords[1][0] == w:
            xinc *= -1
            bounce += 1
        elif cords[0][1] == 0 or cords[3][1] == h:
            yinc *= -1
            bounce += 1
    print(status, bounce-1, steps/v)


if __name__ == '__main__':
    testcases = [
        (8, 3, 0, 0, 1),
        (15, 4, 0, 0, 2),
        (10, 7, 3, 2, 1)]
    for t in testcases:
        calc(*t)
