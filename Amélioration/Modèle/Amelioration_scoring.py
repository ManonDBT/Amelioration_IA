import os
import numpy as np
import pandas as pd
from sklearn import tree
import math
from sklearn import metrics
from sklearn.model_selection import train_test_split

imdb = pd.read_csv("/Amélioration/Data/movies2.csv", encoding="latin-1")

def convert_to_int(string):
    integer = 0
    try:
        integer = int(string)
    except:
        string = string.lower()
        for i in string:
            integer += ord(i)
    return integer


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
    
X_train, X_test, y_train, y_test = train_test_split (X,y, test_size = 0.3, random_state=42)

model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
    

realisateur = input("Entrer le nom d'un réalisateur ")
realisateur = realisateur.lower()
realisateur = convert_to_int(realisateur)

acteur_1 = input("Entrer le nom d'un premier acteur ")
acteur_1 = acteur_1.lower()
acteur_1 = convert_to_int(acteur_1)

acteur_2 = input("Entrer le nom d'un second acteur ")
acteur_2 = acteur_2.lower()
acteur_2 = convert_to_int(acteur_2)

genre = input("Entrer le genre du film ")
genre = genre.lower()
genre = convert_to_int(genre)


prediction = model.predict([[genre, acteur_1, realisateur, acteur_2]])

print('le metascore du film serait :',prediction[0]/10)
