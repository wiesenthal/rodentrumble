
def select(prompt_text = 'Select an option', *options, index=False, info_full=None):
    i = input(prompt_text + ' [' + ', '.join(options) + ']: ')
    if info_full is None:
        while not i in options:
            print(i, ' is not an acceptable input. Try again.')
            i = input(prompt_text + ' [' + ', '.join(options) + ']: ')
        if not index:
            return i
        else:
            return options.index(i)
    else:
        while True:
            info = {k: v[0] for k, v in info_full.items()}
            if i not in options and i not in ['info_' + k for k in info]:
                print(i + " is not an acceptable input. Try again. You can type info_option to learn more. (e.g. info_" + options[0] + ")")
                i = input(prompt_text + ' [' + ', '.join(options) + ']: ')
            elif i in ['info_' + k for k in info]:
                if info_full[i[5:]][1] > -1:
                    print(info[i[5:]] + '\nuses remaining: ' + str(info_full[i[5:]][1]))
                else:
                    print(info[i[5:]])
                i = input(prompt_text + ' [' + ', '.join(options) + ']: ')
            else:
                if not index:
                    return i
                else:
                    return options.index(i)

def wait(prompt_text = 'Press enter to continue'):
    i = input(prompt_text + '...')

def clear():
    print('\n'*1000)