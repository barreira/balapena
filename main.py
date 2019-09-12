import requests
import re
import imdb
from bs4 import BeautifulSoup
from collections import OrderedDict


def remove_suffixes(titles):
    suffixes = ['imax', 'atmos', '4dx', '3d', '(leg)', '(dob)', 'extended']
    res = []

    for t in titles:
        parts = t.split()
        parts = [p for p in parts if p.lower() not in suffixes]

        # Takes care of the trailing '-' in e.g. "Vingadores: Endgame - Extended"
        if parts[-1] == '-':
            parts = parts[:-1]

        res.append(' '.join(parts))

    return list(set(res))


def get_ratings(titles):
    ia = imdb.IMDb()
    ratings = {}

    for t in titles:
        info = ia.search_movie(t)

        if not info:
            ratings[t] = -1  # movie has not been found
            continue

        id = info[0].getID()
        more_info = ia.get_movie(id)

        try:
            rating = more_info['rating']
            ratings[t] = rating
        except KeyError:
            ratings[t] = -2  # movie has no user rating yet

    return ratings


def main():
    r = requests.get('http://cinemas.nos.pt/pages/cartaz.aspx')

    soup = BeautifulSoup(r.content, 'lxml')

    titles = soup.findAll('a', {'class': 'list-item', 'href': re.compile('.*Filmes.*')})
    titles = [t.contents.pop() for t in titles]
    titles = remove_suffixes(titles)

    ratings = get_ratings(titles)
    ratings = OrderedDict(sorted(ratings.items(), key=lambda x: x[1], reverse=True))  # order dict by rating
    ratings = {k: 'N/A (movie has not been found)' if v == -1 else v for k, v in ratings.items()}  # not found message
    ratings = {k: 'N/A (movie has no rating yet)' if v == -2 else v for k, v in ratings.items()}  # not rated message

    for movie, rating in ratings.items():
        print(movie, '-->', rating)


if __name__ == '__main__':
    main()
