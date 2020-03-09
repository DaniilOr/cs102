import pymorphy2
from nltk.corpus import stopwords
from math import log
import re
import string
import pymorphy2
import nltk
table = str.maketrans(dict.fromkeys(string.punctuation))
morph = pymorphy2.MorphAnalyzer()
stop_words = stopwords.words('english')

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.coder = {}
        self.p_s = {}
        self.alpha = alpha

    @staticmethod
    def remove_stopwords(text):
        re.sub("(\s\d+)","", text)
        text.translate(table)
        text = text.lower().split()

        #text.extend(nltk.bigrams(text))
        return [word for word in text if not word in stop_words]

    @staticmethod
    def lemmatization(text):
        return [morph.parse(word)[0].normal_form for word in text]

    @staticmethod
    def my_cool_preprocessing(X):
        #for vector in X:
        #filtred_x.append(self.lemmatization(self.remove_stopwords(X)))#vector)))
        return NaiveBayesClassifier.lemmatization(NaiveBayesClassifier.remove_stopwords(X))

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        filtred_x = X #self.my_cool_preprocessing(X)
        for cl in y:
            if not cl in self.coder.keys():
                self.coder[cl] = len(self.coder)
        classified = {}
        for i in range(len(y)):
            if self.coder[y[i]] not in classified.keys():
                classified[self.coder[y[i]]] = [filtred_x[i]]
            else:
                classified[self.coder[y[i]]].append(filtred_x[i])
        all_words = set()
        for i in range(len(filtred_x)):
            all_words.update(set(filtred_x[i]))
        # words = {
        #     key: [word for text in classified[key] for word in text]
        #     for key in classified
        # }
        words = {}
        for key in classified.keys():
            words[key] = [word for text in classified[key] for word in text]

        for word in all_words:
            self.p_s[word] = []
            for key in classified.keys():
                self.p_s[word].append(words[key].count(word))
            n_all = sum(self.p_s[word])
            for i in range(len(self.p_s[word])):
                self.p_s[word][i] = log((self.p_s[word][i] + self.alpha)
                                         / (n_all + self.alpha*len(all_words)))

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        filtred_x = X#self.my_cool_preprocessing(X)
        predictions = []
        for i in range(len(filtred_x)):
            sums = []
            sums.extend([0] * len(self.coder.keys()))
            for word in filtred_x[i]:
                if word in self.p_s.keys():
                    for index in range(len(self.p_s[word])):
                        sums[index] += self.p_s[word][index]
            predictions.append(sums.index(max(sums)))
        for index in range(len(predictions)):
            predictions[index] = self.match(predictions[index])
        return predictions

    def match(self, prediction):
        for key, value in self.coder.items():
            if value == prediction:
                #print(value, key)
                return key

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        result = 0
        predictions = self.predict(X_test)
        #print(predictions)
        for i in range(len(y_test)):
            if y_test[i] == predictions[i]:
                result += 1
        return result / len(y_test)

if __name__ == '__main__':
    clf = NaiveBayesClassifier()
    X = ['I love this sandwich', 'this is an amazing place','I feel very good about these beers', 'this is my best work', 'What an awesome view', 'I do not like this restaurant', 'I am tired of this stuff', 'I cant deal with this', 'He is my sworn enemy','My boss is horrible']
    y = []
    y.extend(['pos'] * 5)
    y.extend(['neg'] * 5)
    clf.fit(X, y)
    print(clf.score(clf.predict(['The beer was good', 'I do not enjoy my job', 'I aint feeling dandy today', 'I feel amazing', 'Gary is a friend of mine', 'I cant believe Im doing this']), [0, 1, 1, 0, 0, 1]))
