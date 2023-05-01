import pickle


def read():
    with open('data.txt', 'rb') as x:
        data = pickle.load(x)
    return data
