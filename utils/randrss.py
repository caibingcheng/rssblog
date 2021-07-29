import random

def randrss(data, cnt):
    choice = random.sample(data, cnt)
    choice.sort(key=lambda item: item['tmstamp'], reverse=True)

    return choice