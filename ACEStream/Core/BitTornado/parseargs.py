#Embedded file name: ACEStream\Core\BitTornado\parseargs.pyo
from types import *
from cStringIO import StringIO

def splitLine(line, COLS = 80, indent = 10):
    indent = ' ' * indent
    width = COLS - (len(indent) + 1)
    if indent and width < 15:
        width = COLS - 2
        indent = ' '
    s = StringIO()
    i = 0
    for word in line.split():
        if i == 0:
            s.write(indent + word)
            i = len(word)
            continue
        if i + len(word) >= width:
            s.write('\n' + indent + word)
            i = len(word)
            continue
        s.write(' ' + word)
        i += len(word) + 1

    return s.getvalue()


def formatDefinitions(options, COLS, presets = {}):
    s = StringIO()
    for longname, default, doc in options:
        s.write('--' + longname + ' <arg>\n')
        default = presets.get(longname, default)
        if type(default) in (IntType, LongType):
            try:
                default = int(default)
            except:
                pass

        if default is not None:
            doc += ' (defaults to ' + repr(default) + ')'
        s.write(splitLine(doc, COLS, 10))
        s.write('\n\n')

    return s.getvalue()


def usage(string):
    raise ValueError(string)


def defaultargs(options):
    l = {}
    for longname, default, doc in options:
        if default is not None:
            l[longname] = default

    return l


def parseargs(argv, options, minargs = None, maxargs = None, presets = {}):
    config = {}
    longkeyed = {}
    for option in options:
        longname, default, doc = option
        longkeyed[longname] = option
        config[longname] = default

    for longname in presets.keys():
        config[longname] = presets[longname]

    options = []
    args = []
    pos = 0
    while pos < len(argv):
        if argv[pos][:2] != '--':
            args.append(argv[pos])
            pos += 1
        else:
            if pos == len(argv) - 1:
                usage('parameter passed in at end with no value')
            key, value = argv[pos][2:], argv[pos + 1]
            pos += 2
            if not longkeyed.has_key(key):
                usage('unknown key --' + key)
            longname, default, doc = longkeyed[key]
            try:
                t = type(config[longname])
                if t is NoneType or t is StringType:
                    config[longname] = value
                elif t is IntType:
                    config[longname] = int(value)
                elif t is LongType:
                    config[longname] = long(value)
                elif t is FloatType:
                    config[longname] = float(value)
                elif t is BooleanType:
                    config[longname] = bool(value)
                else:
                    print 'parseargs: unknown type is', t
            except ValueError as e:
                usage('wrong format of --%s - %s' % (key, str(e)))

    for key, value in config.items():
        if value is None:
            usage('Option --%s is required.' % key)

    if minargs is not None and len(args) < minargs:
        usage('Must supply at least %d args.' % minargs)
    if maxargs is not None and len(args) > maxargs:
        usage('Too many args - %d max.' % maxargs)
    return (config, args)


def test_parseargs():
    try:
        parseargs([], [('a', 'x', '')])
    except ValueError:
        pass

    try:
        parseargs(['--a', 'x'], [])
    except ValueError:
        pass

    try:
        parseargs(['--a'], [('a', 'x', '')])
    except ValueError:
        pass

    try:
        parseargs([], [], 1, 2)
    except ValueError:
        pass

    try:
        parseargs(['x', 'y', 'z'], [], 1, 2)
    except ValueError:
        pass

    try:
        parseargs(['--a', '2.0'], [('a', 3, '')])
    except ValueError:
        pass

    try:
        parseargs(['--a', 'z'], [('a', 2.1, '')])
    except ValueError:
        pass
