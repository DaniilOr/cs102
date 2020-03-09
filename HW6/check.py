import string
import csv
from bayes import NaiveBayesClassifier
from sklearn.model_selection import train_test_split
with open("SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))
def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)
X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [NaiveBayesClassifier.my_cool_preprocessing(clean(x).lower()) for x in X]
#print(X)
#print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1337)#X[:3900], y[:3900], X[3900:], y[3900:]
model = NaiveBayesClassifier(alpha=0.05)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
#print(predictions)
print(model.score(X_test, y_test))
