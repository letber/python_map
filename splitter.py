"""Module made for splitting big files into smaller \
with reading each n-th line of original file and \
writing it into new file
    """

def splitter(source: str, step: int) -> None:
    with open(source, 'rb') as file:
        lines = file.readlines()[14:]
    
    splitted_lines = []
    for line in lines[::step]:
        splitted_lines.append(str(line, 'ISO-8859-1'))

    return splitted_lines


if __name__ == '__main__':
    step = int(input('Please, enter step: '))
    films_list = splitter('locations.list', step)
    with open(f'locations_{step}.list', 'w') as file:
        file.writelines(films_list)
