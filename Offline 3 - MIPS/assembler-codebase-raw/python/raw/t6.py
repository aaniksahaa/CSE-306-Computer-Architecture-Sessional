def binary_to_hex(bin_str):
    h = hex(int(bin_str,2))[2:]
    while(len(h) < 4):
        h = "0" + h 
    return h 

print(binary_to_hex("0000001100110001"))