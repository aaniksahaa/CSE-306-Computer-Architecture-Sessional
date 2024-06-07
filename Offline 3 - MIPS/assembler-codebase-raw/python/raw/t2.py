a = '$t0'

def get_4_bit_binary(n):
    b = bin(n)[2:]
    while(len(b) < 4):
        b = "0" + b
    return b

register_table = [
    ("$zero", 0),
    ("$t0", 1),
    ("$t1", 2),
    ("$t2", 3),
    ("$t3", 4),
    ("$t4", 5),
    ("$sp", 6)
]

register_address_dict = {reg: address for reg, address in register_table}

def get_register_id(register):
    return register_address_dict.get(register,-1)

def get_register_address(register):
    return get_4_bit_binary(get_register_id(register))

print(get_register_address('$t4'))