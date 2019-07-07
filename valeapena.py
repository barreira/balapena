import requests
import re
import imdb
from bs4 import BeautifulSoup


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
            ratings[t] = 'N/A'

    return ratings


def main():
    url = 'http://cinemas.nos.pt/pages/cartaz.aspx'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'lxml')

    titles = soup.findAll('a', {'class': 'list-item', 'href': re.compile('.*Filmes.*')})
    titles = [t.contents.pop() for t in titles]

    titles = remove_suffixes(titles)
    ratings = get_ratings(titles)

    for movie, rating in ratings.items():
        print(movie, '-->', rating)


if __name__ == '__main__':
    main()
