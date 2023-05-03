import pickle
import os

from session import Session
from locales.ru import ru_locale
from locales.en import en_locale
from config import ACTIVES_PATH, LOCALES_PATH, SESSIONS_PATH


def read_locales():
    with open(LOCALES_PATH, 'rb') as fp:
        data = pickle.load(fp)
    for k in data.keys():
        if data[k] == 'ru':
            data[k] = ru_locale
        elif data[k] == 'en':
            data[k] = en_locale
    return data


def write_to_locales(user_id, locale):
    data = read_locales()
    data[user_id] = locale
    with open(LOCALES_PATH, 'wb') as fp:
        pickle.dump(data, fp)


def read_sessions():
    with open(SESSIONS_PATH, 'rb') as fp:
        data = pickle.load(fp)
    for k in data.keys():
        data[k] = {}
        for title in data[k].keys():
            data[k][title] = Session(*data[k][title], title)
    return data


def write_to_sessions(user_id, session: Session):
    data = read_sessions()
    if user_id not in data:
        data[user_id] = {}
    data[user_id][session.title] = [
        session.context,
        session.virgin,
        session.lang
    ]
    with open(SESSIONS_PATH, 'wb') as fp:
        pickle.dump(data, fp)


def read_actives():
    with open(ACTIVES_PATH, 'rb') as fp:
        data = pickle.load(fp)
    return data


def write_to_actives(user_id, value):
    data = read_actives()
    data[user_id] = value
    with open(ACTIVES_PATH, 'wb') as fp:
        pickle.dump(data, fp)
