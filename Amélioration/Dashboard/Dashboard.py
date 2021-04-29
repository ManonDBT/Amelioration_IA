from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from explainerdashboard import ClassifierExplainer, ExplainerDashboard
from explainerdashboard.datasets import titanic_survive, feature_descriptions
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


imdb = pd.read_csv("Amélioration/Data/movies2.csv", encoding="latin-1")

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

X = pd.DataFrame(X)
y = pd.DataFrame(y)

X = pd.DataFrame(np.array(X), columns = ['Genre', 'Realisateur', 'Acteur_1','Acteur_2'])
y = pd.DataFrame(np.array(y), columns = ['metascore'])
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=42)

model = RandomForestClassifier().fit(X_train, y_train)
explainer = ClassifierExplainer(model, X_test, y_test)

db = ExplainerDashboard(explainer, title="Metascore de film",
                    whatif=False, # you can switch off tabs with bools
                    shap_interaction=False,
                    decision_trees=False)

ExplainerDashboard(explainer).run()