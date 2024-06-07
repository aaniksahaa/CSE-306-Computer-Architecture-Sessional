
debug_instructions = True  

# end of instructions  -->  1111 0000 0000 0001
endmarker_machine_code = "1111000000000001"

# ---------------
# Defined Classes
# ---------------


class Statement:
    def __init__(self, label, instr_name, args, comment):
        self.label = label
        self.instr_name = instr_name
        self.args = args
        self.comment = comment

    def __str__(self):
        return '\t'.join([self.label, self.instr_name, str(self.args), self.comment])
        #return f"Label: {self.label}\tInstruction: {self.instr_name}\tArguments: {self.args}\tComment: {self.comment}"

class Instruction:
    def __init__(self, instr_name, args, instr_no, line_no):
        self.instr_name = instr_name
        self.args = args
        self.instr_no = instr_no
        self.line_no = line_no

    def __str__(self):
        return '\t'.join([self.instr_name, str(self.args)])
        #return f"Instruction: {self.instr_name}\tArguments: {self.args}"



# --------------------
# Input Specifications
# --------------------


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

register_table = [
    ("$zero", 0),
    ("$t0", 1),
    ("$t1", 2),
    ("$t2", 3),
    ("$t3", 4),
    ("$t4", 5),
    ("$sp", 6),
    ("$hd", 7)  # hidden register
]

# Assigned permutation to group G1-A1
permutation = "JDNKLIMFEOPBGCHA"

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

# dictionary for storing ontrol bits 
operation_binary = {'add': '000000000110', 'addi': '000100000100', 'sub': '001000000110', 'subi': '001100000100', 'and': '011000000110', 'andi': '011100000100', 'or': '010000000110', 'ori': '010100000100', 'sll': '101100000100', 'srl': '110100000100', 'nor': '100000000110', 'lw': '000100101100', 'sw': '000100010000', 'beq': '001001000000', 'bneq': '001010000000', 'j': '000000000001'}


# --------------------
# Global Dictionaries
# --------------------


register_id_dict = {}
label_to_address_dict = {}
instruction_dict = {}
order_dict = {}



# --------------------
# Helping Functions
# --------------------

def read_txt(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
    return lines

def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def binary_to_hex(bin_str):
    h = hex(int(bin_str,2))[2:]
    while(len(h) < 4):
        h = "0" + h 
    return h 

def get_8_bit_binary(n):
    n_bits = 8
    # handling 2's complement for negative number
    if(n < 0):
        n = ((2**n_bits)+n)
        
    b = bin(n)[2:]
    while(len(b) < n_bits):
        b = "0" + b
    return b


def get_4_bit_binary(n):
    n_bits = 4
    # handling 2's complement for negative number
    if(n < 0):
        n = ((2**n_bits)+n)
        
    b = bin(n)[2:]
    while(len(b) < n_bits):
        b = "0" + b
    return b

def initialize():
    global instruction_dict
    global order_dict
    global register_id_dict

    instruction_dict = {instr: id for id, instr in instruction_table}

    # for key, value in instruction_dict.items():
    #     print(f"{key}: {value}")

    order_dict = {letter: index for index, letter in enumerate(permutation)}

    # for letter, order in order_dict.items():
    #     print(f"{letter}: {order}")

    register_id_dict = {reg: address for reg, address in register_table}

    # for register, id in register_id_dict.items():
    #     print(f"{register}: {id}")

def get_id(instr_name):
    return instruction_dict.get(instr_name,'')

def get_opcode(instr_name):
    order = order_dict.get(get_id(instr_name),-1)
    # should not be -1
    opcode = get_4_bit_binary(order)
    return opcode 

def get_register_id(register):
    return register_id_dict.get(register,-1)

def get_register_address(register):
    return get_4_bit_binary(get_register_id(register))

def parse_single_line(line):
    label = ''
    instr_name = ''
    args = []
    comment = ''

    instr = ''

    # extracting the comment
    if('#' in line):
        instr = line.split('#',1)[0].strip()
        comment = line.split('#',1)[1].strip()
    else:
        instr = line.strip()

    # extracting the label
    if(':' in instr):
        label = instr.split(':')[0].strip()
        instr = instr.split(':')[1].strip()

    if(len(instr) > 0):
        instr_name = instr.split(' ',1)[0].strip()
        if(len(instr.split(' '))>1):
            args = instr.split(' ',1)[1].strip().replace(' ','').split(',')

    return label, instr_name, args, comment

def parse_statements(statements):
    instructions = []
    pending_label = ''

    # fixing label number alteration due to push-pop
    label_offset = 0

    for i in range(len(statements)):
        statement = statements[i]
        label = statement.label
        instr_name = statement.instr_name
        args = statement.args

        if(len(label) > 0):
            if(label_to_address_dict.get(label,-1) != -1):
                print('Error: Duplicate labels')
            pending_label = label

        if(len(instr_name) > 0):
            if(len(pending_label) > 0):
                label_to_address_dict[pending_label] = len(instructions) + label_offset
                pending_label = ''
            instr = Instruction(instr_name, args, len(instructions) + label_offset , i+1)
            instructions.append(instr)
        
        # fixing label number alteration due to push-pop
        if(instr_name == 'push' and '(' not in args[0]):
            label_offset += 1
        elif(instr_name == 'push' and '(' in args[0]):
            label_offset += 2
        elif(instr_name == 'pop'):
            label_offset += 1
        
        # print(i, instr_name, label_offset)
    
    if(pending_label != ''):
        # an extra end-marker instruction will be added later in the code
        label_to_address_dict[pending_label] = len(instructions) + label_offset

    return instructions, label_to_address_dict

def convert_single_instruction(instr):
    error_msg = ''
    instr_name = instr.instr_name
    args = instr.args

    machine_code = ''

    # R-type instructions
    if(instr_name in ['add','sub','and','or','nor']):
        if(len(args) != 3):
            error_msg = 'Wrong number of arguments'
            return error_msg, machine_code
        else:
            for register in args:
                if(get_register_id(register) == -1):
                    error_msg = 'Invalid register name'
                    return error_msg, machine_code
            
            # for valid input
                
            machine_code = get_opcode(instr_name)
            # source reg 1
            machine_code += get_register_address(args[1])
            # source reg 2
            machine_code += get_register_address(args[2])
            # destination reg
            machine_code += get_register_address(args[0])

    # S-type instructions
    elif(instr_name in ['sll','srl']):
        if(len(args) != 3):
            error_msg = 'Wrong number of arguments'
            return error_msg, machine_code
        else:
            for register in args[:2]:
                if(get_register_id(register) == -1):
                    error_msg = 'Invalid register name'
                    return error_msg, machine_code

            # for valid input
                
            machine_code = get_opcode(instr_name)
            # source reg 
            machine_code += get_register_address(args[1])
            # destination reg
            machine_code += get_register_address(args[0])
            #shamt
            machine_code += get_4_bit_binary(int(args[2]))

    # I-type immediate instructions       
    elif(instr_name in ['addi','subi','andi','ori']):
        if(len(args) != 3):
            error_msg = 'Wrong number of arguments'
            return error_msg, machine_code
        else:
            for register in args[:2]:
                if(get_register_id(register) == -1):
                    error_msg = 'Invalid register name'
                    return error_msg, machine_code

            # for valid input
                
            machine_code = get_opcode(instr_name)
            # source reg 
            machine_code += get_register_address(args[1])
            # destination reg
            machine_code += get_register_address(args[0])
            # immediate
            machine_code += get_4_bit_binary(int(args[2]))

    # I-type branch instructions       
    elif(instr_name in ['beq','bneq']):
        if(len(args) != 3):
            error_msg = 'Wrong number of arguments'
            return error_msg, machine_code
        else:
            for register in args[:2]:
                if(get_register_id(register) == -1):
                    error_msg = 'Invalid register name'
                    return error_msg, machine_code
            
            # for valid input
                
            machine_code = get_opcode(instr_name)
            # source reg 1
            machine_code += get_register_address(args[0])
            # source reg 2
            machine_code += get_register_address(args[1])

            # address (PC relative)
            label = args[2]
            if(label not in label_to_address_dict):
                error_msg = 'Invalid label'
                return error_msg, machine_code
            
            absolute_address = label_to_address_dict[label]
            relative_address = absolute_address - ((instr.instr_no) + 1)
            print(absolute_address,((instr.instr_no) + 1),relative_address)
            if(relative_address > 7 or relative_address < -8):
                error_msg = 'Branch offset exceeds 4 bit boundary, relative address must be between -8 and 7'
                return error_msg, machine_code

            machine_code += get_4_bit_binary(relative_address)

    # I-type lw, sw instructions       
    elif(instr_name in ['lw','sw']):
        if(len(args) != 2):
            error_msg = 'Wrong number of arguments'
            return error_msg, machine_code
        else:  
            reg2 = args[0]
            if(len(args[1].split('(')) != 2):
                error_msg = 'Wrong offset format'
                return error_msg, machine_code
            
            reg1 = args[1].split('(')[1].split(')')[0]
            offset = args[1].split('(')[0]

            machine_code = get_opcode(instr_name)
            # source reg 1
            machine_code += get_register_address(reg1)
            # source reg 2
            machine_code += get_register_address(reg2)
            # offset
            machine_code += get_4_bit_binary(int(offset))

    # J-type instruction      
    elif(instr_name in ['j']):
        if(len(args) != 1):
            error_msg = 'Wrong number of arguments'
            return error_msg, machine_code
        else:  
            # address (absolute)
            label = args[0]
            if(label not in label_to_address_dict):
                error_msg = 'Invalid label'
                return error_msg, machine_code
            
            absolute_address = label_to_address_dict[label]

            machine_code = get_opcode(instr_name)
            # absolute_address
            machine_code += get_8_bit_binary(absolute_address)
            #zero padding
            machine_code += "0000"
    
    else:
        error_msg = 'Invalid instruction name ' + instr_name
        return error_msg, machine_code

    return error_msg, machine_code    

def convert_push(instr):
    if(instr.instr_name != 'push'):
        print("\n\nUNEXPECTED ERROR, not a push instruction\n\n")
    dummy_1 = Instruction('subi',['$sp','$sp','1'],instr.instr_no,instr.line_no)
    dummy_2 = Instruction('sw',[instr.args[0],'0($sp)'],instr.instr_no,instr.line_no)
    return dummy_1, dummy_2

def convert_push_memory(instr):
    if(instr.instr_name != 'push'):
        print("\n\nUNEXPECTED ERROR, not a push instruction\n\n")
    dummy_1 = Instruction('subi',['$sp','$sp','1'],instr.instr_no,instr.line_no)
    dummy_2 = Instruction('lw',['$hd',instr.args[0]],instr.instr_no,instr.line_no)
    dummy_3 = Instruction('sw',['$hd','0($sp)'],instr.instr_no,instr.line_no)
    return dummy_1, dummy_2, dummy_3

def convert_pop(instr):
    if(instr.instr_name != 'pop'):
        print("\n\nUNEXPECTED ERROR, not a pop instruction\n\n")
    dummy_1 = Instruction('lw',[instr.args[0],'0($sp)'],instr.instr_no,instr.line_no)
    dummy_2 = Instruction('addi',['$sp','$sp','1'],instr.instr_no,instr.line_no)
    return dummy_1, dummy_2

"""

id = 0

while(id < len(my_list)):
    # print(my_list)
    if(my_list[id] == 2):
        # Remove the current element
        removed_element = my_list.pop(id)

        # Insert two elements at the same position
        my_list.insert(id, '99')
        my_list.insert(id + 1, '100')
        id -= 1
    else:
        print(my_list[id])
    id += 1

"""


def parse_instructions(instructions):
    machine_codes = []
    error_occurred = False
    at = 0
    while(at < len(instructions)):
        instr = instructions[at]
        if(instr.instr_name == 'push' and '(' not in instr.args[0]):
            dummy_1, dummy_2 = convert_push(instr)
            removed = instructions.pop(at)
            instructions.insert(at, dummy_1)
            instructions.insert(at+1, dummy_2)
            at -= 1
        elif(instr.instr_name == 'push' and '(' in instr.args[0]):
            dummy_1, dummy_2, dummy_3 = convert_push_memory(instr)
            removed = instructions.pop(at)
            instructions.insert(at, dummy_1)
            instructions.insert(at+1, dummy_2)
            instructions.insert(at+2, dummy_3)
            at -= 1
        elif(instr.instr_name == 'pop'):
            dummy_1, dummy_2 = convert_pop(instr)
            removed = instructions.pop(at)
            instructions.insert(at, dummy_1)
            instructions.insert(at+1, dummy_2)
            at -= 1
        else:
            error_msg, machine_code = convert_single_instruction(instr)
            if(len(error_msg) > 0):
                print('\nError at line ' + str(instr.line_no) + ': ' + error_msg+'\n')
                error_occurred = True
            else: 
                if(debug_instructions):
                    print(instr, machine_code)
                machine_codes.append(machine_code)
            #print(error_msg, machine_code)
        at += 1
    machine_codes.append(endmarker_machine_code)
    return error_occurred, machine_codes

def get_statements(lines):
    statements = []
    for line in lines:
        label, instr_name, args, comment = parse_single_line(line)

        # print('\t'.join([label, instr_name, str(args), comment]))
        statement = Statement(label, instr_name, args, comment)
        #print(statement)

        statements.append(statement)
    return statements

def write_binary(machine_codes):
    text = ""
    for machine_code in machine_codes:
        text += machine_code + '\n'
    write_txt('machine-code-binary.txt',text)

def write_hex(machine_codes):
    text = ""
    for machine_code in machine_codes:
        text += binary_to_hex(machine_code).upper() + '\n'
    write_txt('machine-code-hex.txt',text)

def write_assembly(assembly_filename):
    lines = read_txt(assembly_filename)
    statements = get_statements(lines)
    instructions, label_to_address_dict = parse_statements(statements)
    error_occurred, machine_codes = parse_instructions(instructions)

    if(not error_occurred):
        # print(machine_codes)
        write_binary(machine_codes)
        write_hex(machine_codes)
        print('\nMachine Code written successfully.')
        return True
    else:
        print('\n\nSorry\nERROR occurred during parsing\n\n')
        return False

def write_instructions_array():
    machine_code_hex_filename = 'machine-code-hex.txt'

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

    print('\nInstruction array written successfully.')


def get_3_bit_hex(b):
    h = hex(int("0b" + b,2))[2:]
    while(len(h) < 3):
        h = "0" + h
    h = "0x" + h
    return h

def write_controls_array():
    control_filename = 'control_hex_array.txt'

    hex_controls = []

    for letter in permutation:
        op = instruction_table[ord(letter) - ord('A')][1]
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

    print('\nControl hex array written successfully.\n')

    #print(s)

# ------------------
# Debugger Functions
# ------------------
    
def debug():
    print('\nMapping from label to PC:\n')
    print(label_to_address_dict)
    # for label, pc in label_to_address_dict:
    #     print(label + ' -> ' + str(pc))
    # print()

# ---------------
# Input Filename
# ---------------

assembly_filename = 'assembly.txt'


# ---------
# Assembler
# ---------

# def convert_push(instr):
#     if(instr.instr_name != 'push'):
#         print("\n\nUNEXPECTED ERROR, not a push instruction\n\n")
#     dummy_1 = Instruction('sw',[instr.args[0],'0($sp)'],instr.instr_no,instr.line_no)
#     dummy_2 = Instruction('subi',['$sp','$sp','1'],instr.instr_no,instr.line_no)
#     return dummy_1, dummy_2

# def convert_pop(instr):
#     if(instr.instr_name != 'pop'):
#         print("\n\nUNEXPECTED ERROR, not a pop instruction\n\n")
#     dummy_1 = Instruction('lw',[instr.args[0],'0($sp)'],instr.instr_no,instr.line_no)
#     dummy_2 = Instruction('addi',['$sp','$sp','1'],instr.instr_no,instr.line_no)
#     return dummy_1, dummy_2

initialize()
success = write_assembly(assembly_filename)
if(success):
    write_instructions_array()
    write_controls_array()

debug()





