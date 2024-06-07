import json 

def read_txt(filename):
    with open(filename,'r', encoding='utf-8') as f:
        data = f.read()
    return data

def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def print_as_json(data):
    json_string = json.dumps(data, indent=4)
    print(json_string)

data = read_txt("input.txt")
lines = data.split("\n")

n = len(lines)

lines.insert(0,"")

components = []

at_line = 3

for line_number in range(at_line,n+1):
    at_line = line_number
    line = lines[line_number].strip()
    if(line == '#'):
        break 
    components.append(line)


components = list(set(components))

print(at_line)

at_line += 2

error = False

directed_graph = {}

while(at_line <= n):
    line = lines[at_line].strip()
    if(line == 'END'):
        break 
    if(line not in components):
        print("Error: " + line + " is not a predefined component")
        break
    at_line += 2
    u = line
    directed_graph[u] = []
    while(at_line <= n):
        line = lines[at_line].strip()
        if(line == '#'):
            break 
        v = line.split(' ')[0]
        cnt = int(line.split(' ')[1])
        directed_graph[u].append([v,cnt])
        at_line += 1
    at_line += 1


print_as_json(directed_graph)
print(components)

leaves = []

for c in components:
    if(c not in directed_graph):
        leaves.append(c)

print(leaves)

# get individual leaf counts for one instance of this component
def dfs(u):   
    #print(u)                          
    leaf_counts = {}

    for leaf in leaves:
        leaf_counts[leaf] = 0

    if(u in leaves):  # leaf
        leaf_counts[u] = 1
        return leaf_counts

    for [v,cnt] in directed_graph[u]:
        child_leaf_counts = dfs(v)
        for leaf in leaves:
            leaf_counts[leaf] += cnt*(child_leaf_counts[leaf])
    
    return leaf_counts

root = "FPA"
leaf_counts = dfs(root)

print_as_json(leaf_counts)

result = ""
total = 0

for ic in leaf_counts:
    cnt = leaf_counts.get(ic,0)
    result += ic + " " + str(cnt)
    result += "\n"
    total += cnt

result += "\nTotal = " + str(total)

print(result)

write_txt("output.txt", result)