def genericError(text, line):
    error = 'ERROR: %s. Line %d' % (text, line)
    return error

def notDefinedError(t, name, line):
    error = 'ERROR: %s %s does not exist. Line %d' % (t, name, line)
    return error

def expectedError(expected, got, line):
    error = 'ERROR: expected %s. Got %s instead. Line %d' % (expected, got, line)
    return error

def printErrors(errors):
    for e in errors:
        print(e)