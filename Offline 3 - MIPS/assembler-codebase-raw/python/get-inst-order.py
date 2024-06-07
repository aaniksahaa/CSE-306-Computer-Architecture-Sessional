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

# Create a dictionary with letters as keys and instructions as values
instruction_dict = {letter: instruction for letter, instruction in instruction_table}


s = ""

for letter in permutation:
    s += instruction_dict[letter] + "\n"

write_txt("inst-order.txt",s)