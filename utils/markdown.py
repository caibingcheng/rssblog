import requests

def markdown(path, locale=True):
    if locale:
        with open(path, 'r') as f:
            return f.read()
    else:
        return requests.get(path).text