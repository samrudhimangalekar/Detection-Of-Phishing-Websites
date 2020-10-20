import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
#import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import re
from IPython.display import display
pd.options.display.max_rows=None
from IPython.display import display, Markdown
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from pandas.plotting import scatter_matrix
from matplotlib import cm



#Importing dataset
data = np.loadtxt("dataset.csv", delimiter = ",")

#Seperating features and labels
X = data[: , :-1]
y = data[: , -1]
    
#split training and testing data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#Support Vector Machine
from sklearn.svm import SVC
svm = SVC()
svm.fit(X_train, y_train)
acc1=svm.score(X_train, y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'.format(acc1))
print('Accuracy of SVM classifier on test set: {:.2f}'.format(svm.score(X_test, y_test)))

pred = svm.predict(X_test)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

#Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
acc2=gnb.score(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'.format(acc2))
print('Accuracy of GNB classifier on test set: {:.2f}'.format(gnb.score(X_test, y_test)))

pred = gnb.predict(X_test)
confusion_mat=confusion_matrix(y_test, pred)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

from sklearn.ensemble import RandomForestClassifier

# Create the model with 100 trees
model = RandomForestClassifier(n_estimators=100, 
                               bootstrap = True,
                               max_features = 'sqrt')
# Fit on training data
model.fit(X_train, y_train)
acc3=model.score(X_train, y_train)
print('Accuracy of Rf classifier on training set: {:.2f}'.format(acc3))
print('Accuracy of Rf classifier on test set: {:.2f}'.format(model.score(X_test, y_test)))

pred = model.predict(X_test)
confusion_mat=confusion_matrix(y_test, pred)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

#Logistic regression 
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
acc4=logreg.score(X_train, y_train)
print('Accuracy of Logistic regression classifier on training set: {:.2f}'.format(acc4))
print('Accuracy of Logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

pred = logreg.predict(X_test)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

#cmp=classification_report(y_test, pred).split()
#cmp1=cmp[-4:]
acc=[acc1,acc2,acc3,acc4]
classifiers=['SVM','Naive_bayes','Random_Forest','Logistic']
y_pos=np.arange(len(classifiers))
plt.bar(y_pos,acc,color=['black','red','blue','green'])
plt.xticks(y_pos,classifiers)
plt.show()