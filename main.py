import requests
import re
import imdb
from bs4 import BeautifulSoup
from collections import OrderedDict


def remove_suffixes(titles):
    suffixes = ['imax', 'atmos', '4dx', '3d', '(leg)', '(dob)']
    res = []

    for t in titles:
        parts = t.split()
        parts = [p for p in parts if p.lower() not in suffixes]
        res.append(' '.join(parts))

    return list(set(res))


def get_ratings(titles):
    ia = imdb.IMDb()
    ratings = {}

    for t in titles:
        info = ia.search_movie(t)
        id = info[0].getID()
        more_info = ia.get_movie(id)

        try:
            rating = more_info['rating']
            ratings[t] = rating
        except KeyError:
            ratings[t] = -1  # if movie has no user rating yet

    return ratings


def main():
    r = requests.get('http://cinemas.nos.pt/pages/cartaz.aspx')

    soup = BeautifulSoup(r.content, 'lxml')

    titles = soup.findAll('a', {'class': 'list-item', 'href': re.compile('.*Filmes.*')})
    titles = [t.contents.pop() for t in titles]
    titles = remove_suffixes(titles)

    ratings = get_ratings(titles)
    ratings = OrderedDict(sorted(ratings.items(), key=lambda x: x[1], reverse=True))  # order dict by rating
    ratings = {k: 'N/A' if v == -1 else v for k, v in ratings.items()}  # use 'N/A' instead of -1 if no rating available

    for movie, rating in ratings.items():
        print(movie, '-->', rating)


if __name__ == '__main__':
    main()
