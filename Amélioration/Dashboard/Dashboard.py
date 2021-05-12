from explainerdashboard.explainers import RandomForestRegressionExplainer
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
from explainerdashboard import ClassifierExplainer, ExplainerDashboard, RegressionExplainer
from explainerdashboard.datasets import titanic_survive, feature_descriptions
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


imdb = pd.read_csv("Amélioration/Data/movies2.csv", encoding="latin-1")
imdb = imdb.rename(columns = {'11:14' :'film','7.2' : 'metascore','Crime' : 'genre', 'Greg Marcks':'realisateur', 	'Henry Thomas' : 'acteur_1', 'Colin Hanks':'acteur_2' ,'6000000' : 'budget',	'0': 'votes2',	'0.1': 'vote',	'Aug 12, 2005': 'date'})
colonne = ['genre','acteur_1', 'acteur_2', 'realisateur']
imdb = pd.get_dummies(imdb, columns= colonne)
imdb = imdb.drop(columns= ['film', 'budget', 'votes2', 'vote', 'date'], axis = 1 )


X = imdb.loc[:, imdb.columns != 'metascore' ]
y = imdb.loc[:, imdb.columns == 'metascore' ]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=42)

model = RandomForestRegressor().fit(X_train, y_train)
explainer = RegressionExplainer(model, X_test, y_test)

db = ExplainerDashboard(explainer, title="Metascore de film",
                    whatif=False, # you can switch off tabs with bools
                    shap_interaction=False,
                    decision_trees=False)

ExplainerDashboard(explainer).run()