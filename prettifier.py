""" Prettify a string"""

def prettify_string(in_string):
    """
    Make a string human readable
    :param in_string: the raw string
    :return: the prettified string.
    """
    in_string = in_string.replace('\\', '').replace('/\"', '\"')
    out_line = ""

    counter_curly = 0

    for char in in_string:

        if char == '{':
            out_line += ('\n' + counter_curly * '\t' + char)
            counter_curly += 1
            continue
        if char == ',':
            out_line += char + ('\n' + counter_curly * '\t')
            continue
        if char == '}':
            counter_curly -= 1
            out_line += '\n' + counter_curly * '\t' + char

            continue

        out_line += char

    return out_line
