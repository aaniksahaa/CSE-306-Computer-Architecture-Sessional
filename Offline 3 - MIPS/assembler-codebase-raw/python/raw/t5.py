def get_4_bit_binary(n):
    # handling 2's complement for negative number
    if(n < 0):
        n = (16+n)

    b = bin(n)[2:]
    while(len(b) < 4):
        b = "0" + b
    return b

print(get_4_bit_binary(0))