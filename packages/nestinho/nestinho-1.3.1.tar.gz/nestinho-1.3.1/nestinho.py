def print_lol(the_list, indent, level=0): #We turned second argument into a optional argument.
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)
