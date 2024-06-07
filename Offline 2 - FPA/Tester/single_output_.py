import random


def export(lines, file):
    f = open(file, 'w')
    f.write('v2.0 raw\n')
    for line in lines:
        f.write(line + '\n')
    f.close()


def pad_left(x, n):
    while len(x) != n:
        x = "0" + x
    return x


def pad_right(x, n):
    while len(x) != n:
        x = x + "0"
    return x


def get_random_exp():
    x = random.randint(1, 5) + 1023
    b = bin(x)[2:]
    b = pad_left(b, 11)
    return b


def get_random_frac():
    x = random.randint(1, 100)
    b = bin(x)[2:]
    b = pad_right(b, 20)
    return b


def get_random_float():
    f = "0"
    f += get_random_exp()
    f += get_random_frac()
    return f

def print_float(x):
    print(x[0],end=' ')
    print(x[1:12], end= ' ')
    print(x[12:], end='\t')
    print(get_fraction(x), end=' ')
    print(get_exponent(x), end=' ')
    print(to_decimal(x))


def add_float(x, y):
    Ex = int(x[1:12], 2) - 1023
    Ey = int(y[1:12], 2) - 1023
    if Ey < Ex:
        Ex, Ey = Ey, Ex
        x, y = y, x
    d = Ey - Ex
    fx = int("01"+x[12:], 2)
    fy = int("01"+y[12:], 2)
    # print_float(x)
    # print_float(y)

    # print("fx = ", fx)
    # print("fy = ", fy)

    Ex += d
    fx >>= d
    f = fx + fy

    F = ""
    for i in range(0, 22, 1):
        if (f & (1 << i)) != 0:
            F += "1"
        else:
            F += "0"
    F = F[::-1]

    print(len(F))

    F = pad_right(F, 100)
    j=0
    for i in range(22):
        if F[i] == '1':
            j = i
            break
    Ex += 1-j
    F = F[j+1:j+21]

    # print(len(F))

    E = ""
    Ex += 1023
    for i in range(0, 11, 1):
        if (Ex & (1 << i)) != 0:
            E += "1"
        else:
            E += "0"
    E = E[::-1]
    r = "0" + E + F
    # print_float(r)
    return r

def get_fraction(x):
    f = x[12:]
    r = 1
    for i in range(len(f)):
        if f[i] == '1':
            r += 2 ** -(i+1)
    return r

def get_exponent(x):
    e = int(x[1:12], 2) - 1023
    return e

def to_decimal(x):
    e = int(x[1:12], 2) - 1023
    f = x[12:]
    r = 1
    for i in range(len(f)):
        if f[i] == '1':
            r += 2 ** -(i+1)
    r *= 2 ** e
    return r


a = "01000000010011000110000000000000"
b = "01000000000011111000000000000000"

# print(to_decimal(a))
# print(to_decimal(b))

ans = add_float(a,b)

h = hex(int(ans,2))[2:]

# print(len(ans))

print(h)
