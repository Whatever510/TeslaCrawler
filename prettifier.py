def prettify_string(in_string):
    in_string = in_string.replace('\\', '').replace('/\"', '\"')
    out_line = ""

    counter_curly = 0

    for c in in_string:

        if c == '{':
            out_line += ('\n' + counter_curly * '\t' + c)
            counter_curly += 1
            continue
        if c == ',':
            out_line += c + ('\n' + counter_curly * '\t')
            continue
        if c == '}':
            counter_curly -= 1
            out_line += '\n' + counter_curly * '\t' + c

            continue

        out_line += c

    return out_line
