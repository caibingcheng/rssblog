def markdown(ps, key, path):
    with open(path, 'r') as f:
        ps[key] = f.read()

    return ps