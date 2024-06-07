class Statement:
    def __init__(self, label, instr_name, args, comment):
        self.label = label
        self.instr_name = instr_name
        self.args = args
        self.comment = comment

    def __str__(self):
        return f"Label: {self.label}\nInstruction Name: {self.instr_name}\nArguments: {self.args}\nComment: {self.comment}"

# Example usage:
statement1 = Statement("L1", "ADD", ["R1", "R2", "R3"], "Addition")
print(statement1)
