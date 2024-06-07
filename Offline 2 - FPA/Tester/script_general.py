import random

# Number of sign bits = 1
eb = 11  # Number of bits in exponent
fb = 32-1-eb  # Number of bits in fraction
appendage = "01"
ab = len(appendage)   # Number of extra appended bits ( in our case, it is 2, "01" is appended )

bias = 2**(eb-1)-1

def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def export(lines, file):
    text = ''
    text += 'v2.0 raw\n'
    for line in lines:
        text += line + '\n'
    write_txt(file, text)


def pad_left(x, n):
    while len(x) != n:
        x = "0" + x
    return x


def pad_right(x, n):
    while len(x) != n:
        x = x + "0"
    return x


def get_random_exp():
    x = random.randint(1, 5) + bias 
    b = bin(x)[2:]
    b = pad_left(b, eb)
    return b


def get_random_frac():
    x = random.randint(1, 100)
    b = bin(x)[2:]
    b = pad_right(b, fb)
    return b


def get_random_float():
    f = "0"
    f += get_random_exp()
    f += get_random_frac()
    return f

def print_float(x):
    print(x[0],end=' ')
    print(x[1:(eb+1)], end= ' ')
    print(x[(eb+1):], end='\t')
    print(get_fraction(x), end=' ')
    print(get_exponent(x), end=' ')
    print(to_decimal(x))

def add_float(x, y):
    Ex = int(x[1:(eb+1)], 2) - bias 
    Ey = int(y[1:(eb+1)], 2) - bias 

    if Ey < Ex:
        Ex, Ey = Ey, Ex
        x, y = y, x

    d = Ey - Ex

    fx = int(appendage+x[(eb+1):], 2)
    fy = int(appendage+y[(eb+1):], 2)

    Ex += d
    fx >>= d

    f = fx + fy

    F = ""
    for i in range(0, ab+fb, 1):
        if (f & (1 << i)) != 0:
            F += "1"
        else:
            F += "0"
    F = F[::-1]

    # print(len(F))

    F = pad_right(F, 100)
    j=0
    for i in range(ab+fb):
        if F[i] == '1':
            j = i          # finding leading 1
            break
    Ex += 1-j
    F = F[j+1:j+(fb+1)]

    # print(len(F))

    E = ""
    Ex += bias 
    for i in range(0, eb, 1):
        if (Ex & (1 << i)) != 0:
            E += "1"
        else:
            E += "0"
    E = E[::-1]
    r = "0" + E + F
    # print_float(r)
    return r

def get_fraction(x):
    f = x[(eb+1):]
    r = 1
    for i in range(len(f)):
        if f[i] == '1':
            r += 2 ** -(i+1)
    return r

def get_exponent(x):
    e = int(x[1:(eb+1)], 2) - bias 
    return e

def to_decimal(x):
    e = int(x[1:(eb+1)], 2) - bias 
    f = x[(eb+1):]
    r = 1
    for i in range(len(f)):
        if f[i] == '1':
            r += 2 ** -(i+1)
    r *= 2 ** e
    return r

def generate_correct_output(ram_bits):
    test = (2**ram_bits)
    X = []
    Y = []
    Z = []
    for t in range(test):
        x = get_random_float()
        y = get_random_float()
        z = add_float(x, y)
        hx = hex(int(x,2))[2:]
        hy = hex(int(y,2))[2:]
        hz = hex(int(z,2))[2:]
        X.append(hx)
        Y.append(hy)
        Z.append(hz)

    path = 'output/'

    export(X, path+'x.txt')
    export(Y, path+'y.txt')
    export(Z, path+'z.txt')

def generate_wrong_output(ram_bits):
    ratio = 4                 # 1 wrong for every four
    test = (2**ram_bits)
    X = []
    Y = []
    Z = []
    for t in range(test):
        x = get_random_float()
        y = get_random_float()
        z = add_float(x, y)
        hx = hex(int(x,2))[2:]
        hy = hex(int(y,2))[2:]
        hz = hex(int(z,2))[2:]
        if(t % ratio == 0):
            hy, hz = hz, hy 
        X.append(hx)
        Y.append(hy)
        Z.append(hz)

    path = 'wrong/'

    export(X, path+'x.txt')
    export(Y, path+'y.txt')
    export(Z, path+'z.txt')


ram_bits = 8

generate_correct_output(ram_bits)
generate_wrong_output(ram_bits)
