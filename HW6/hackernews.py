from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import nltk
import pickle


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    line = s.query(News).filter(News.id == request.query['id']).first()
    line.label = request.query['label']
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    page = 1
    flag = False
    while(True):
        news = get_news('https://news.ycombinator.com/newest', page)[(page - 1) * 30:]
        for new in news:
            if not s.query(News).filter(News.author == new['author']). \
                                 filter(News.title == new['title']). \
                                 first() is None:
                flag = True
                break
            else:
                n = News(title = new['title'],
                         author = new['author'],
                         url = new['url'],
                         comments = new['comments'],
                         points = new['score'])
                s.add(n)
                s.commit()
        if flag:
            break
        page += 1
    redirect("/news")


def is_all_news(request):
    return request.query['type'] == '0'


def is_good(item):
    return item.label == 'good'



@route("/classify")
def classify_news():
    #clf = NaiveBayesClassifier()
    s = session()
    training = s.query(News).filter(News.label != None).all()
    #print(type(training))
    X_train, y = process(training)
    '''clf.fit(X_train, y)
    with open('data.pickle', 'wb') as f:
        pickle.dump(clf, f)
    '''
    with open('data.pickle', 'rb') as f:
        clf = pickle.load(f)
    rows = s.query(News).filter(News.label == None).all()
    X_test, _ = process(rows)
    predictions = clf.predict(X_test)
    for i, row in enumerate(rows):
        row.label = predictions[i]

    if is_all_news(request):
        rows.sort(key=lambda row: row.label)
        #print(len(rows))
    else:
        rows = [row for row in rows if is_good(row)]
        #print(len(new_rows))
        #rows = new_rows
    return template('news_template', rows=rows)


def process(data):
    X, y, authors, urls = [], [], [], []
    for item in data:
        X.append(item.title)
        y.append(item.label)
        authors.append(item.author)
        new_item = item.url
        try:
            new_item = new_item.split('//')[1].split('/')[0]
        except:
            new_item = item.url
        finally:
            urls.append(new_item)

    X_train = []
    for i in range(len(X)):
        sub_arr = NaiveBayesClassifier.my_cool_preprocessing(X[i])
         #sub_arr.extend(nltk.bigrams(sub_arr))
        sub_arr.extend([authors[i], urls[i]])
        X_train.append(sub_arr)
    return X_train, y


@route("/auto")
def auto():
    s = session()
    good = ['nasa', 'python', 'musk', 'gates', 'virus', 'ml', 'deep learning', 'ai', 'pandemi', 'ban', 'trump', 'tutorial', 'video', 'study', 'scientific', 'dark', 'money']
    bad = ['economy', 'java', 'c#', 'thinking', '3d', 'engine','intrnet', 'bubble', 'gov', 'test', 'functional', 'apple', 'html', 'argue', 'static', 'women', 'woman', 'hash', 'astrology', 'atom', 'google', 'hn', 'manage']
    rows = s.query(News).filter(News.label == None).all()
    for item in rows:
        print(item.title.lower())
        flag = False
        for word in good:
            if word in item.title.lower():
                print(item.title.lower(), 'good')
                item.label = 'good'
                s.commit()
                flag = True
                break
        if not flag:
            for word in bad:
                if word in item.title.lower():
                    print(item.title.lower(), 'never')
                    item.label='never'
                    s.commit()
                    flag = True
            if not flag:
                print(item.title.lower(), 'MB')
                item.label = 'maybe'
                s.commit()




if __name__ == "__main__":
    run(host="localhost", port=8080)
