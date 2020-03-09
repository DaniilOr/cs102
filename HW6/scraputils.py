import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    for title in parser.find_all('td', {'class': 'title'}):
        new = {}
        a = title.find('a', {'class': 'storylink'})
        if not a is  None:
            new['title'] = a.contents[0]
            new['url'] = a.get('href')
            news_list.append(new)
    subs = parser.find_all('td', {'class': 'subtext'})
    for i in range(len(subs)):
        score = subs[i].find('span', {'class': 'score'})
        score = score.contents[0].replace('s','').replace(' point', '')
        news_list[i]['score'] = int(score)
        author = subs[i].find_all('a')[0].contents[0]
        comm = subs[i].find_all('a')[-1].contents[0].replace('\xa0comment', '')
        comments = int(comm.replace('s', '')) if not 'discuss' in comm else 0
        news_list[i]['author'] = author
        news_list[i]['comments'] = comments
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find('a', {'class': 'morelink'}).get('href')


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

if __name__ == '__main__':
    get_news('https://news.ycombinator.com/newest', 10)
