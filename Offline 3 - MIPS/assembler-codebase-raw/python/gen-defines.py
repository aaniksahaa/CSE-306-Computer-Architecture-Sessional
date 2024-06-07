def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

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

# Generate a dictionary mapping instruction to its position in the permutation
instruction_position_dict = {instruction: permutation.index(letter) for letter, instruction in instruction_table}

s = ""

# Generate the desired code
for instruction, position in instruction_position_dict.items():
    s += f"# define {instruction} 0x{position:02X}\n"

write_txt("defines.txt",s)





