import os
import sys
import logging
import pandas as pd

import mlflow
from mlflow.tracking import MlflowClient

from dataclasses import dataclass

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt
from Amelioration_scoring import convert_to_int

@dataclass
class Parameters:
   # Preprocessing parameeters
   data_name: str
   data_path: str = f"data"
   model_path: str = f"model"
   k_folds: int = 10
   test_size: float = 0.1

class Pipeline:
   def __init__(self, params):
      self.params = params
      self.dataset_path = f"{params.data_path}/{params.data_name}.csv"
      self.dataset = None
      self.x = None
      self.y = None
      self.x_train = None
      self.x_test = None
      self.y_train = None
      self.y_test = None
      
      self.best_max_depth = None
      self.best_grid = None
      self.best_splitter = None
      self.tree = None

   def load_data(self):
      # Read dataset
      self.dataset = pd.read_csv("/Amélioration/Data/movies2.csv", encoding="latin-1")
      
      # Save artifact
      mlflow.log_artifact(f"{self.dataset}")
      
   def preprocessing(self):
       imdb = self.dataset.values.tolist()
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
   
   def split_data(self):
      self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x,self.y, test_size=self.params.test_size)
      
   def parameter_tuning(self):
      # Defining parameters grid
      parameters = {'criterion': ['gini','entropy'], 'splitter': ['best','random']}
      
      # Grid search
      tree = DecisionTreeClassifier()
      grid = GridSearchCV(tree, parameters, cv=self.params.k_folds)
      grid.fit(self.x_train, self.y_train)
      
     
      self.best_criterion = grid.best_params_['criterion']
      self.best_splitter = grid.best_params_['splitter']
         
      mlflow.log_param(f'best_max_depth', self.best_max_depth)
      mlflow.log_param(f'best_criterion', self.best_criterion)
      mlflow.log_param(f'best_splitter', self.best_splitter)
      
   def k_fold_cross_validation(self):
      
      self.tree = DecisionTreeClassifier( splitter=self.best_splitter, criterion=self.best_criterion)
      kfold_scores = cross_val_score(self.tree, self.x_train, self.y_train, cv=self.params.k_folds)
      
      mlflow.log_metric(f"average_accuracy", kfold_scores.mean())
      mlflow.log_metric(f"std_accuracy", kfold_scores.std())
      
   def model_evaluation(self):
      
      self.tree.fit(self.x_train, self.y_train)
   
      mlflow.log_metric(f"train_accuracy", self.tree.score(self.x_train, self.y_train))
      mlflow.log_metric(f"test_accuracy", self.tree.score(self.x_test, self.y_test))
      
    def save_model(self):
    # Creates the tree topology
    
        fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=300)
        tree.plot_tree(self.tree)
         # Save the tree
        fig.savefig(f"{self.params.img_path}/tree_{self.params.data_name}.png")
         
         # Track the optimum model
        mlflow.sklearn.save_model(self.tree, f"{self.params.model_path}/sklearn_{data_name}", serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_PICKLE)
         # Track the decision tree image
        mlflow.log_artifact(f"{self.params.img_path}/tree_{self.params.data_name}.png")


if __name__ == '__main__':
   # If data name is provided by commanda line, success
   # If data name is not provided, shows an exception
   try:
      # Gets data name from command line
      data_name = sys.argv[1]
   except:
      print(f"You must provide a dataname, please try:\npython main.py [dataname]")

   # Init parameters
   params = Parameters(data_name)
   if os.path.isfile(f"{params.data_path}/{params.data_name}.csv"):

      # Initi Mlflow client
      client = MlflowClient()
      
      # If the project does not exists, it creates a new one
      # If the project already exists, it is taken the project id
      try:
         # Creates a new experiment
         experiment_id = client.create_experiment(data_name)
         # logging.info(f"The experiment {data_name} was created with id={experiment_id} ")
      except:
         # Retrieves the experiment id from the already created project
         experiment_id = client.get_experiment_by_name(data_name).experiment_id
         # logging.info(f"The id={experiment_id} from experiment {data_name} was retrieved successfully")
      
      # Initialize mlflow context
      with mlflow.start_run(experiment_id=experiment_id, run_name='test_mushroom'):
         # Pipeline execution
         pipeline = Pipeline(params)
         pipeline.load_data()
         pipeline.preprocessing()
         pipeline.split_data()
         pipeline.parameter_tuning()
         pipeline.k_fold_cross_validation()
         pipeline.model_evaluation()
         pipeline.save_model()

