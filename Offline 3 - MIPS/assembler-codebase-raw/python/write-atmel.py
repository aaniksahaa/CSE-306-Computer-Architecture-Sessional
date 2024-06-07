with open('machine-code-hex.txt', 'r') as file:
    hex_strings = file.read().splitlines()

first_two_chars = [hex_string[:2] for hex_string in hex_strings]
last_two_chars = [hex_string[-2:] for hex_string in hex_strings]

n = len(first_two_chars)

# print("First two chars array:", first_two_chars)
# print("Last two chars array:", last_two_chars)

f2 = ""
f2 += "{ "

for i in range(n):
    s = first_two_chars[i]
    f2 += "0x" + s
    if(i != (n-1)):
        f2 += ", "

f2 += " }"

print(f2)



l2 = ""
l2 += "{ "

for i in range(n):
    s = last_two_chars[i]
    l2 += "0x" + s
    if(i != (n-1)):
        l2 += ", "

l2 += " }"

print(l2)