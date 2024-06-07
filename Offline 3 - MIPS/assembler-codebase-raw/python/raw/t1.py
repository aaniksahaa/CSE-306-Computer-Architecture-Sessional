# Instruction table as per specification
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

# Assigned permutation to group G1-A1
permutation = "JDNKLIMFEOPBGCHA"

# Global dictionaries
instruction_dict = {}
order_dict = {}

def initialize():
    global instruction_dict
    global order_dict

    instruction_dict = {instr: id for id, instr in instruction_table}

    # for key, value in instruction_dict.items():
    #     print(f"{key}: {value}")

    order_dict = {letter: index for index, letter in enumerate(permutation)}

    # for letter, order in order_dict.items():
    #     print(f"{letter}: {order}")

def get_id(instr_name):
    return instruction_dict.get(instr_name,'')

def get_opcode(instr_name):
    order = order_dict.get(get_id(instr_name),-1)
    # should not be -1
    opcode = bin(order)[2:]
    return opcode 

initialize()
print(get_opcode('ori'))