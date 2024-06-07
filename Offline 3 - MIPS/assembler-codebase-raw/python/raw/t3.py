def get_4_bit_binary(n):
    b = bin(n)[2:]
    while(len(b) < 4):
        b = "0" + b
    return b

print(get_4_bit_binary(15))