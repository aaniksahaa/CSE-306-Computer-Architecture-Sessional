lines = [
    '        addi $t1, $zero, 3		    # $t1 = 3 ',
    '# MIPS assembly code',
    '        j end                       ',
    'label1:	sll $t3, $t3, 1	            # $t3 = 2	',
    '       j           ',
    '        lw $t2, 4($t2)		        # $t2 = 3	'
]

def parse_single_line(line):
    is_empty = False
    is_error = False 

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

    if(len(instr)==0):
        is_empty = True
    else:
        instr_name = instr.split(' ',1)[0].strip()
        if(len(instr.split(' '))>1):
            args = instr.split(' ',1)[1].strip().replace(' ','').split(',')

    return label, instr_name, args, comment

for line in lines:
    label, instr_name, args, comment = parse_single_line(line)
    print('\t'.join([label, instr_name, str(args), comment]))