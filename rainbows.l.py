import sys

variables = {}
special_chars = {
    '!t':'\t',
    '!n':'\n',    
    }
flags = {
    'loop':False,
    }

loop_params = []

def evaluate(line):
    tokens = line.split(' ')
    if tokens[0] == 'set':
        #set var_name var_type var_dat
        #variables[var_name] = [var_type, var_dat]
        var_tokens = tokens[1:]
        if var_tokens[2] == 'inp':
            var_name, var_type = var_tokens[0:2]
            inp_str = ' '.join(var_tokens[3:])
            var_dat = input(inp_str)
            variables[var_name] = [var_type,var_dat]
        elif var_tokens[1] == 'var':
            var_name, var2_name = var_tokens[0], var_tokens[2]
            var2_type, var2_dat = variables[var2_name]
            variables[var_name] = [var2_type,var2_dat]
        elif len(var_tokens) == 3:
            var_name, var_type, var_dat = var_tokens
            variables[var_name] = [var_type,var_dat]

    if tokens[0] == 'print':
        #print str lol, hi!
        #|
        #+->['str', 'lol,' ,'hi!']
        #    |   |  |            |
        #    +-+-+  +------+-----+
        #      |           |
        #      |            +-> print_dat
        #      +-> print_dat_type
        print_dat_type, print_dat = tokens[1],tokens[2:]
        if print_dat_type == 'str':
            print_dat = ' '.join(print_dat)
            for special_char in special_chars.keys():
                if special_char in print_dat:
                    print_dat = print_dat.replace(special_char,special_chars[special_char])
            sys.stdout.write(print_dat)
        if print_dat_type == 'num':
            sys.stdout.write(print_dat[0])
        if print_dat_type == 'var':
            print_var_name = print_dat[0]
            print_var_dat_type, print_var_dat = variables[print_var_name][0],variables[print_var_name][1]
            evaluate('print {0} {1}'.format(print_var_dat_type, print_var_dat))

    if tokens[0] == 'add':
        # add vname 12
        #   sets the variable vname to the value of vname+12
        # add vname var v2name
        #   sets variable vname to the value of vname + the value of v2name
        var_name = tokens[1]
        var_value = float(variables[var_name][1])
        add_tokens = tokens[2:]
        if len(add_tokens) == 1:
            value_to_add = float(add_tokens[0])
        if len(add_tokens) == 2:
            if add_tokens[0] == 'var':
                var2_name = add_tokens[1]
                value_to_add = float(variables[var2_name][1])
        variables[var_name] = ['num',str(var_value+value_to_add)]

    if tokens[0] == 'mult':
        # mult vname 12
        #   sets the variable vname to the value of vname*12
        # add vname var v2name
        #   sets variable vname to the value of vname + the value of v2name
        var_name = tokens[1]
        var_value = float(variables[var_name][1])
        mult_tokens = tokens[2:]
        if len(mult_tokens) == 1:
            value_to_mult = float(mult_tokens[0])
        if len(mult_tokens) == 2:
            if mult_tokens[0] == 'var':
                var2_name = mult_tokens[1]
                value_to_mult = float(variables[var2_name][1])
        variables[var_name] = ['num',str(var_value*value_to_mult)]

    if tokens[0] == 'loop':
        #loop [line_start] [line_finish] [loop_n_times]
        #loop [line_start] [line_finish] var [var_name]
        global loop_params
        loop_tokens = tokens[1:]
        if loop_tokens[2] == 'var':
            loop_var_name = loop_tokens[3]
            loop_var_dat = variables[loop_var_name][1]
            loop_params = [int(loop_token) for loop_token in [loop_tokens[0],loop_tokens[1],loop_var_dat]]
        else:
            loop_params = [int(token) for token in loop_tokens]
        flags['loop'] = True
            
    return

def main():

    with open('fib_test.txt', 'r') as file:
        code = file.read()
    
    lines = code.split('\n')
    current_line = 0
    while current_line < len(lines):
        if flags['loop'] != True:
            line = lines[current_line]
            evaluate(line)
            current_line += 1
        elif flags['loop'] == True:
            loop_run = 0
            loop_line_start, loop_line_end, loop_n = loop_params
            while loop_run < loop_n:
                current_loop_line = loop_line_start
                while current_loop_line <= loop_line_end:
                    evaluate(lines[current_loop_line])
                    current_loop_line += 1
                loop_run += 1
            flags['loop'] = False

if __name__ == '__main__':
    main()
