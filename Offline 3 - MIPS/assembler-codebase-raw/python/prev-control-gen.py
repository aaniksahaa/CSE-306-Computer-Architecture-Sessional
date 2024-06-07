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

# Display the dictionary
print(operation_binary)