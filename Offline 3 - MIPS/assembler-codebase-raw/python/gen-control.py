
# get operation binaries.....


# Define the operations and their corresponding indices
operations = {
    "add": 0x0D,
    "addi": 0x03,
    "sub": 0x0E,
    "subi": 0x04,
    "and": 0x0B,
    "andi": 0x02,
    "or": 0x07,
    "ori": 0x08,
    "sll": 0x06,
    "srl": 0x00,
    "nor": 0x0F,
    "lw": 0x05,
    "sw": 0x01,
    "beq": 0x0C,
    "bneq": 0x0A,
    "j": 0x09
}

# Control memory array
controlMem = [0xd04, 0x110, 0x704, 0x104, 0x304, 0x12c, 0xb04, 0x406,
               0x504, 0x001, 0x280, 0x606, 0x240, 0x006, 0x206, 0x806]

# Create a dictionary to store operations and their binary values
operation_binary = {}

# Iterate through each operation and retrieve its corresponding binary value
for op, index in operations.items():
    binary_value = bin(controlMem[index])[2:].zfill(12)  # Convert to binary and zero-fill to 12 bits
    operation_binary[op] = binary_value


"""

Meanings of control bits (0 = LSB)

0 - not jump / jump
1 - write destination select (rt / rd)
2 - regwrite
3 - memread
4 - memwrite
5 - write-data-select (ALUout or Read Data from memory)
6 - beqf
7 - bneqf
8 - ALU operand select (rt / address,immediate)

"""

operation_binary = {'add': '000000000110', 'addi': '000100000100', 'sub': '001000000110', 'subi': '001100000100', 'and': '011000000110', 'andi': '011100000100', 'or': '010000000110', 'ori': '010100000100', 'sll': '101100000100', 'srl': '110100000100', 'nor': '100000000110', 'lw': '000100101100', 'sw': '000100010000', 'beq': '001001000000', 'bneq': '001010000000', 'j': '000000000001'}

#---------------------------



instruction_table = [
    ("A", "add"),
    ("B", "addi"),
    ("C", "sub"),
    ("D", "subi"),
    ("E", "and"),
    ("F", "andi"),
    ("G", "or"),
    ("H", "ori"),
    ("I", "sll"),
    ("J", "srl"),
    ("K", "nor"),
    ("L", "sw"),
    ("M", "lw"),
    ("N", "beq"),
    ("O", "bneq"),
    ("P", "j"),
]

permutation = "JDNKLIMFEOPBGCHA"

# Create a dictionary with letters as keys and instructions as values
instruction_dict = {letter: instruction for letter, instruction in instruction_table}

def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def get_3_bit_hex(b):
    h = hex(int("0b" + b,2))[2:]
    while(len(h) < 3):
        h = "0" + h
    h = "0x" + h
    return h

def write_controls_array(control_filename):
    hex_controls = []

    for letter in permutation:
        op = instruction_dict[letter]
        binary_controls = operation_binary[op]
        h = get_3_bit_hex(binary_controls)
        #print(h)
        hex_controls.append(h)

    s = "\n{ "

    m = len(hex_controls)

    for i in range(m):
        s += hex_controls[i]
        if(i<m-1):
            s += ", "

    s += " }\n"

    write_txt(control_filename,s)

    #print(s)

control_filename = 'control_hex_array.txt'
write_controls_array(control_filename)



