import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score, mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


import mlflow
import mlflow.sklearn
from urllib.parse import urlparse

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def eval_metrics(y_test, y_pred):
    f1 = f1_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    precision = precision_score(y_test, y_pred, average='macro')
    acc = accuracy_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return f1, recall, precision, acc, rmse, mae, r2
 

def convert_to_int(string):  
   integer = 0   
   try:
        integer = int(string)
   except:
        string = string.lower()
        for i in string:
            integer += ord(i)
   return integer
 
if __name__ == "__main__":
   warnings.filterwarnings("ignore")
        
   imdb = pd.read_csv("/Users/manon/Projet/Projet-SIMPLON/Amélioration/Data/movies2.csv", encoding="latin-1")
   imdb = imdb.values.tolist()   
     
   X = []
   y = []
        
   for i in range(len(imdb)):
      X.append([imdb[i][2], imdb[i][3], imdb[i][4], imdb[i][5]]) #Genre, directeur, Acteur 1 et Acteur 2
      y.append(imdb[i][1]) #metascore
            
   for i in range(len(X)):
      for x in range(len(X[i])):
         X[i][x] = convert_to_int(X[i][x])

   for i in range(len(y)):
      y[i] = int(float(y[i])*10)
            
   X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=42)


def fetch_logged_data(run_id):
    client = mlflow.tracking.MlflowClient()
    data = client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in client.list_artifacts(run_id, "model")]
    return data.params, data.metrics, tags, artifacts


# enable autologging
mlflow.sklearn.autolog()


with mlflow.start_run():
    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    (f1, recall, precision, acc, rmse, mae, r2) =  eval_metrics(y_test, y_pred)

    print("  Precision: %s" % precision)
    print("  Recall: %s" % recall)
    print("  F1-score: %s" % f1)
    print("  accuracy: %s" % acc)
    print("  rmse: %s" % rmse)
    print("  mae: %s" % mae)
    print("  r2: %s" % r2)

    mlflow.log_metric("precision", precision)
    mlflow.log_metric("F1-score", f1)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("r2", r2)
      