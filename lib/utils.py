
def shargs(func):
    from inspect import signature as sig
    from sys import argv

    if '.py' in argv[0]:
        del argv[0]
    else:
        del argv[0:1]

    if argv[0] in ('-h', '--help'):
        help(func)
        exit()

    sig = sig(func)
    params = sig.parameters.values()

    args = []
    kwargs = {}

    for par in params:
        key = par.name
        mod = par.kind
        typ = 0

        if len(dir(par.default)) != 26:
            typ = type(par.default)

        elif len(dir(par.annotation)) != 26:
            typ = par.annotation

        if typ not in [str, int, float, bool, list, tuple]:
            del typ

        _arg = par.POSITIONAL_OR_KEYWORD
        _args = par.VAR_POSITIONAL
        _kwargs = par.VAR_KEYWORD

        _pos = par.POSITIONAL_ONLY
        _key = par.KEYWORD_ONLY

        if len(argv) > 0:

            if mod in (_arg, _pos):
                if f'--{key}' in argv:
                    i = argv.index(f'--{key}')

                    if 'typ' in locals():
                        val = typ(argv[i + 1])
                    else:
                        val = argv[i + 1]

                    args.append(val)
                    del argv[i:i+1]

                else:

                    if 'typ' in locals():
                        val = typ(argv[0])
                    else:
                        val = argv[0]

                    args.append(val)
                    del argv[0]

            elif mod == _args:

                s = e = 0
                for a in argv:

                    if 'typ' in locals():
                        val = typ(a)
                    else:
                        val = a

                    if f'--' in a:
                        break
                    else:
                        args.append(val)
                        e += 1

                del argv[s:e]

            else:
                if f'--{key}' in argv:
                    i = argv.index(f'--{key}')

                    if 'typ' in locals():
                        val = typ(argv[i + 1])
                    else:
                        val = argv[i + 1]

                    kwargs[key] = val

    return func(*args, **kwargs)
    