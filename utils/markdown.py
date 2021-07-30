import requests

def markdown(ps, key, path, locale=True):
    if locale:
        with open(path, 'r') as f:
            ps[key] = f.read()
    else:
        ps[key] = requests.get(path).text

    return ps