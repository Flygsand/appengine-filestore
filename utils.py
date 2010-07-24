def chunks(str, size):
    for i in xrange(0, len(str), size):
        yield str[i:i+size]
