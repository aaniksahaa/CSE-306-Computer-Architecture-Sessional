def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def write_instructions_array(machine_code_hex_filename):
    with open(machine_code_hex_filename, 'r') as file:
        hex_strings = file.read().splitlines()

    n = len(hex_strings)

    s = "\n"

    s += "{ "
    for i in range(256):
        if(i < n):
            s += "0x" + hex_strings[i]
        else:
            s += "0x0000"
        if(i < 255):
            s += ", "
    s += " }"

    s += "\n"

    write_txt("instruction_array.txt",s)


machine_code_hex_filename = 'machine-code-hex.txt'
write_instructions_array(machine_code_hex_filename)