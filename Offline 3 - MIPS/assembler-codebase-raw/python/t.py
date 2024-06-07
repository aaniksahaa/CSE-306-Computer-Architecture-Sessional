my_list = [1, 2, 3, 4, 5]

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


print(my_list)
