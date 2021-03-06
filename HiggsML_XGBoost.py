# -*- coding: utf-8 -*-
"""HiggsML_XGBoost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19DA_FPSupXUIjeErez4HErwHz0KNOsTe
"""

from google.colab import drive
drive.mount('/content/gdrive')

import pandas as pd 
df=pd.read_csv('gdrive/My Drive/BE(CSE)/Mega Project!/Dataset/ATLAS Collaboration CERN Dataset.csv')

#Importing Dependencies

import numpy as np
#import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import Imputer, StandardScaler

from time import time

# %matplotlib inline

# Read data from the CSV into a dataframe

#loc = "G:/Z - Priority/Z - Mega Project/Python Code and Dataset/"
#df = pd.read_csv(loc + 'ATLAS Collaboration CERN Dataset.csv')

# Display first 5 rows
df.head()

#Train set

train = df[:250000]

train.tail()

#Test set

test = df[250000:]
test = test.drop(['Weight', 'Label'], axis = 1)

test.head()

#Checking the Missing Values in the train set & test set

cnt1 = train.isnull().sum().sum()
cnt2 = test.isnull().sum().sum()

print(cnt1+cnt2)

X = train.drop(['EventId','Label','Weight'],1)
y = train['Label']

X.head()

#Filling in -999.00(Marker for empty feilds) values with median of the rest of the data in the column

imp = Imputer(missing_values=-999.00, strategy='median')
cols = X.columns
X = pd.DataFrame(imp.fit_transform(X), columns=cols)
X.describe()

#Some features still have a high deviation. Hence scaling all the features

scaler = StandardScaler()
cols = X.columns
X = pd.DataFrame(scaler.fit_transform(X), columns=cols)
X.describe()

"""# Visualization"""

#Count Plot

#y = train['Label']
sns.countplot(y)
print("Percentage of 's' : ",float((sum(y=='s'))/len(y))*100)

sns.boxplot(y = X['DER_mass_MMC'])

"""# Validation"""

# Shuffle and split the dataset into training and testing set.

#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.20,
                                                    random_state = 42,
                                                    stratify = y)

"""#Model Building and Prediction"""

#!pip install -q xgboost==0.4a30
import xgboost as xgb

clf = xgb.XGBClassifier(seed = 82)

clf.fit(X_train, y_train)

start = time()

y_pred = clf.predict(X_train)

end = time()
tr_time = end - start

start = time()

y_pred_2 = clf.predict(X_test)

end = time()
ts_time = end - start

y_pred

y_pred_2

#Import f1_score and accuracy_score from sklearn.metrics

from sklearn.metrics import f1_score, accuracy_score

train_f1_scr = f1_score(y_train , y_pred, pos_label ='s')
train_acc = accuracy_score(y_train , y_pred)

print ("Made predictions in {:.4f} seconds.".format(tr_time))
print ("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(train_f1_scr , train_acc))

test_f1_scr = f1_score(y_test, y_pred_2, pos_label ='s')
test_acc = accuracy_score(y_test , y_pred_2)

print ("Made predictions in {:.4f} seconds.".format(ts_time))
print ("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(test_f1_scr , test_acc))

"""#Optimisation"""

# TODO: Import 'GridSearchCV' and 'make_scorer'
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer


# TODO: Create the parameters list you wish to tune
parameters = { 'learning_rate' : [0.1],
               'n_estimators' : [40],
               'max_depth': [3],
               'min_child_weight': [3],
               'gamma':[0.4],
               'subsample' : [0.8],
               'colsample_bytree' : [0.8],
               'scale_pos_weight' : [1],
               'reg_alpha':[1e-5]
             }  

# TODO: Initialize the classifier
clf = xgb.XGBClassifier(seed=2)

# TODO: Make an f1 scoring function using 'make_scorer' 
f1_scorer = make_scorer(f1_score,pos_label='s')

# TODO: Perform grid search on the classifier using the f1_scorer as the scoring method
grid_obj = GridSearchCV(clf,
                        scoring=f1_scorer,
                        param_grid=parameters,
                        cv=5)

# TODO: Fit the grid search object to the training data and find the optimal parameters
grid_obj = grid_obj.fit(X_train,y_train)

# Get the estimator
clf = grid_obj.best_estimator_
print (clf)

# Report the final F1 score for training and testing after parameter tuning
#f1, acc = predict_labels(clf, X_train, y_train)
#print ("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1 , acc))
    
#f1, acc = predict_labels(clf, X_test, y_test)
#print ("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1 , acc))

start = time()

y_pred = clf.predict(X_train)

end = time()
tr_time = end - start

start = time()

y_pred_2 = clf.predict(X_test)

end = time()
ts_time = end - start

train_f1_scr = f1_score(y_train , y_pred, pos_label ='s')
train_acc = accuracy_score(y_train , y_pred)

print ("Made predictions in {:.4f} seconds.".format(tr_time))
print ("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(train_f1_scr , train_acc))

test_f1_scr = f1_score(y_test, y_pred_2, pos_label ='s')
test_acc = accuracy_score(y_test , y_pred_2)

print ("Made predictions in {:.4f} seconds.".format(ts_time))
print ("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(test_f1_scr , test_acc))

#import matplotlib.pyplot as plt

def gplot(c1,c2):
    # Data to plot
    labels = 'Signal', 'Background'
    sizes = [c1, c2]
    colors = ['gold', 'lightskyblue']
    explode = (0.1, 0)  # explode 1st slice
 
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140) 
    plt.axis('equal')
    plt.show()

c1 = 0
c2 = 0

for i in range(0,len(y_pred)):
        if(y_pred[i] == 's'):
            c1 = c1 + 1
        else:
            c2 = c2 + 1
gplot(c1,c2)

c1 = 0
c2 = 0

for i in range(0,len(y_pred_2)):
        if(y_pred_2[i] == 's'):
            c1 = c1 + 1
        else:
            c2 = c2 + 1
gplot(c1,c2)

