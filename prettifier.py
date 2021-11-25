

def prettify_string(in_string):
    in_string = in_string.replace('\\', '').replace('/\"','\"')
    out_line = ""

    counter_curly = 0
    counter_square = 0
    print = False



    #line = file.readline().replace('\\','')
    index = 0

    for c in in_string:

        if c == '{':
            out_line += ('\n' + counter_curly*'\t' + c )
            counter_curly += 1
            continue
        if c == ',':
            out_line += c + ('\n' + counter_curly*'\t')
            continue
        if c == '}':
            counter_curly -= 1
            out_line += '\n' + counter_curly * '\t' + c

            continue


        out_line += c


        #if print:
            #if index == 1000:
                #print(out_line)
                #break
            #index +=1

    return out_line
