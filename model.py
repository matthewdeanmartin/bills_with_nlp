import itertools

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import itertools

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import io
import requests

input_file = "data.csv"


# comma delimited is the default
df = pd.read_csv(input_file,
                 names=["bill_id", "status", "summary"],
                 encoding='cp1252')





# Use a file that you download
# input_file = "data.csv"
# comma delimited is the default
# df = pd.read_csv(input_file,
#                  names=["bill_id", "status", "summary"],
#                  encoding='cp1252')

# use a premade file
url="https://raw.githubusercontent.com/matthewdeanmartin/bills_with_nlp/main/data.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('cp1252')),
              names=["bill_id", "status", "summary"])

df.head()


# Getting features of dataframe
# Same as SELECT feature1, feature2, feature3 FROM data
# X = data[["feature1", "feature2", "feature3"]]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["summary"])
print(vectorizer.get_feature_names())

y = df['status']  # Labels

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Random forests are a good model for when you have many features and relatively
# few data points (e.g. 10,000s of predictive words, yet only 100s of bills)
clf = RandomForestClassifier(n_estimators=100)

# Train the model using the training sets
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

y_pred.head()

# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print(clf.feature_importances_)
i = 0

# should use pandas way...
importances = list(zip(vectorizer.get_feature_names(), clf.feature_importances_))
importances.sort(key=lambda x:x[1])
importances = filter(lambda score: score[1] > 0, importances)

for feat, importance in itertools.islice(importances, 20):
    if importance == 0:
        continue
    print('feature: {f}, importance: {i}'.format(f=feat, i=importance))


# new_bill_text =
# new_bill = vectorizer.fit_transform()
# ad_hoc = clf.predict([""])


