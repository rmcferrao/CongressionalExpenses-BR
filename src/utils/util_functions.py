def insert_every_n(n, string):
    splitted = string.split(' ')
    len_section = 0
    sections = []
    j = 0

    for i, word in enumerate(splitted):
        len_section += len(word)

        if len_section > n:
            sections.append(' '.join(splitted[j:i+1]))
            len_section = 0
            j = i + 1

    if not sections:
        return string

    if splitted[j:]:
        sections[-1] = ' '.join([sections[-1], *splitted[j:]])

    return '\n'.join(sections)