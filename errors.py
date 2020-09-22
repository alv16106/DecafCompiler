def genericError(text, line):
    error = 'ERROR: Line %d. %s.' % (line, text)
    print(error)
    return error

def notDefinedError(t, name, line):
    error = 'ERROR: Line %d. %s "%s" does not exist.' % (line, t, name)
    print(error)
    return error

def expectedError(expected, got, line):
    error = 'ERROR: Line %d. Expected %s. Got %s instead.' % (line, expected, got)
    print(error)
    return error

def printErrors(errors):
    for e in errors:
        print(e)