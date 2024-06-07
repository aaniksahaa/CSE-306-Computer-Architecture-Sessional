import json

# from MSB to LSB
def get_number_from_binary_array(B):
    ans = 0
    for b in B:
        if(b>1 or b<0):
            print('Invalid Input')
            return -1
        ans *= 2
        ans += b
    return ans

def get_rows_of_truth_table(data):
    # Split the data into lines and remove leading/trailing whitespaces
    lines = [line.strip() for line in data.strip().split('\n')]

    # Extract the column names from the first line
    column_names = lines[0].split()

    # Initialize an empty list to store the dictionaries
    result = []

    # Process each data line and create a dictionary for each row
    for line in lines[1:]:
        values = line.split()
        row_dict = {column_names[i]: int(value) for i, value in enumerate(values)}
        result.append(row_dict)

    return result

def check_attribute_present(row, attr):
    if(attr not in row):
        print('\nSorry! ', attr, ' is not specified for this row')
        print(json.dumps(row,indent=6))
        return False
    return True


def check_row(row, n_bits=4, n_control_bits=3):
    cs = []
    a = []
    b = []
    s = []
    if not check_attribute_present(row, 'Cout'):
        return 0
    s.append(row['Cout'])
    mx = max(n_bits, n_control_bits)
    for i in range(mx-1, -1, -1):
        if(i < n_control_bits):
            id = 'cs'+str(i)
            if not check_attribute_present(row, id):
                return 0
            cs.append(row[id])
        if(i < n_bits):

            id = 'A'+str(i)
            if not check_attribute_present(row, id):
                return 0
            a.append(row[id])

            id = 'B'+str(i)
            if not check_attribute_present(row, id):
                return 0
            b.append(row[id])

            id = 'S'+str(i)
            if not check_attribute_present(row, id):
                return 0
            s.append(row[id])

    control = get_number_from_binary_array(cs)
    A = get_number_from_binary_array(a)
    B = get_number_from_binary_array(b)
    S = get_number_from_binary_array(s)
    
    #print(control, A, B, S)
    
    Y = 0
    
    if(control == 0):
        Y = A + B
    if(control == 1):
        Y = 2**n_bits - A
    if(control == 2):
        Y = A + B
    if(control == 3):
        Y = A + B + 1
    if(control == 4):
        Y = A + 1
    if(control == 5):
        Y = A & B
    if(control == 6):
        Y = A ^ B
    if(control == 7):
        Y = A ^ B
    
    state = 1

    messages = []

    # moment of truth
    if(Y != S):
        messages.append('\nOutput Decimal Value (with considering Cout) should be ' + str(Y) + ', but output is '+ str(S) + '\n')
        # print('Cout = ', row['Cout'])
        state = -1

    # testing flags
    if(('C' in row) and row['C'] != row['Cout']):
        messages.append('\nCarry Flag is incorrect!')
        state = -1

    if(('S' in row) and row['S'] != row['S'+str(n_bits-1)]):
        messages.append('\nSign Flag is incorrect!')
        state = -1
    
    Z_expected = 1
    for i in range(n_bits):
        if(row['S'+str(i)] == 1):
            Z_expected = 0
    
    if(('Z' in row) and row['Z'] != Z_expected):
        messages.append('\nZero Flag is incorrect!')
        state = -1
    
    if('V' in row):
        if(control in [5,6,7]):
            if(row['C'] == 1 or row['V'] == 1):
                messages.append('\nOverflow Flag incorrect.\nC and V should be cleared (0) after AND/OR/XOR operation.')
        else:
            signed_A = A
            if(row['A'+str(n_bits-1)] == 1): # negative, so it is 2's complement
                signed_A = 2**n_bits - A
            
            signed_B = B
            if(row['B'+str(n_bits-1)] == 1): # negative, so it is 2's complement
                signed_B = 2**n_bits - B 

            A = signed_A
            B = signed_B

            if(control == 0):
                Y = A + B
            if(control == 1):
                Y = 2**n_bits - A
            if(control == 2):
                Y = A + B
            if(control == 3):
                Y = A + B + 1
            if(control == 4):
                Y = A + 1

            overflowed = 0

            if((Y > 2**(n_bits-1)-1) or (Y < -2**(n_bits-1))):
                overflowed = 1
            
            if(row['V'] != overflowed):
                messages.append('Overflow bit incorrect')

    if(state == -1):
        print('\n\nOops! Wrong output for control = ', control, ', A = ', A, ', B = ', B)
        for message in messages:
            print(message)
    
    return state
    
# remove any last newline(if any) from txt file  
def read_truth_table(filename):
    with open(filename) as f:
        data = f.read()
    return data

data = read_truth_table('truth_table.txt')
result = get_rows_of_truth_table(data)

#print(json.dumps(result,indent=4))
#print(len(result))

errors = 0
corrupted = 0

for row in result:
    ret = check_row(row)
    if(ret == -1):
        errors += 1
    if(ret == 0):
        corrupted += 1

print('\n\n')
if(errors == 0 and corrupted == 0):
    print('Congrats! All rows of the truth table are correct!')
if(corrupted != 0):
    print('Sorry! ', corrupted, ' rows of the truth table are corrupted. Maybe this is due to anomalous naming convention.\n')
    print('The followed convention:\n\nControl bits = cs0, cs1, cs2\nA = A0, A1 etc\nB = B0, B1 etc\nS = S0, S1 etc\nCout = Cout ')
    if(errors == 0):
        print('\n\nBut non-corrupted rows are all correct!')
if(errors != 0):
    print('Sorry! ', errors, ' rows of the truth table are incorrect.')
print('\n\n')