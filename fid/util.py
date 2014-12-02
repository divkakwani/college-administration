def capitalize_name(name):
    return " ".join(word.capitalize() for word in name.split())

def parseInt(string):
    for index in xrange(len(string)):
        if not string[index].isdigit():
            break
    if index == 0:
        return 0
    return int(string[:index])
