from bottle import (
    route, run, template, request, redirect
)
import re
from scraputils import get_wall
from db import Posts, session
from bayes import NaiveBayesClassifier
import nltk
import pickle


@route("/")
@route("/posts")
def news_list():
    s = session()
    rows = s.query(Posts).filter(Posts.label == None).all()
    '''for item in rows:
        item.text = re.sub('#\w*', '', item.text)
        item.text = re.sub('@\w*', '', item.text)
        if item.text == '':
            s.delete(item)
        s.commit()'''
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    line = s.query(Posts).filter(Posts.id == request.query['id']).first()
    line.label = request.query['label']
    s.commit()
    redirect("/posts")


@route("/update")
def update_news():
    s = session()
    count = 100
    offset = 0
    flag = False
    while(True):
        posts = get_wall(domain = 'pn6', count = count, offset = offset)
        for post in posts:
            if not s.query(News).filter(Posts.text == posts['text']).first() is None:
                flag = True
                break
            else:
                n = Posts(text = post['text'],
                         likes = post['likes'],
                         views = post['views'])
                if precheck(n):
                    s.add(n)
                    s.commit()
        counte += 100
        offset += 100
        if flag:
            break
    redirect("/posts")


@route("/classify")
def classify_news():
    clf = NaiveBayesClassifier()
    s = session()
    training = s.query(Posts).filter(Posts.label != None).all()
    #print(type(training))
    X_train, y = process(training)
    #print(X_train)
    #clf.fit(X_train, y)
    #with open('data.pickle', 'wb') as f:
    #    pickle.dump(clf, f)
    clf = pickle.load(open('data.pickle', 'rb'))
    rows = s.query(Posts).filter(Posts.label == None).all()
    X_test, _ = process(rows)
    predictions = clf.predict(X_test)
    counter = 0
    for row in rows:
        row.label = predictions[counter]
        counter += 1
    rows.sort(key=lambda x: x.label)
    return template('news_template', rows=rows)


def process(data):
    X, y = [], []
    for item in data:
        X.append(item.text)
        y.append(item.label)

    X_train = []
    for i in range(len(X)):
        X_train.append(NaiveBayesClassifier.my_cool_preprocessing(X[i]))
         #sub_arr.extend(nltk.bigrams(sub_arr))
    #print(len(X_train), len(y))
    return X_train, y

def precheck(post):
    post.text = re.sub('#\w*', '', item.text)
    post.text = re.sub('@\w*', '', item.text)
    if item.text == '':
        return False
    else:
        return True

if __name__ == "__main__":
    run(host="localhost", port=8080)
