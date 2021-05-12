# Demo: (Slider, Dropdown, Radio, CheckboxGroup, Checkbox) -> (Textbox)

import gradio as gr
import joblib
import pandas as pd #

model = joblib.load('Amélioration/Modèle/model_amelioration.pkl')
imdb = pd.read_csv("/Users/manon/Projet/Projet-SIMPLON/Amélioration/Data/movies2.csv", encoding="latin-1")
imdb = imdb.rename(columns = {'11:14' :'film','7.2' : 'metascore','Crime' : 'genre', 'Greg Marcks':'realisateur', 	'Henry Thomas' : 'acteur_1', 'Colin Hanks':'acteur_2' ,'6000000' : 'budget',	'0': 'votes2',	'0.1': 'vote',	'Aug 12, 2005': 'date'})

def convert_to_int(string):
    integer = 0
    try:
        integer = int(string)
    except:
        string = string.lower()
        for i in string:
            integer += ord(i)
    return integer


def predict(realisateur, acteur_1, acteur_2, genre):
      realisateur = realisateur.lower()
      realisateur = convert_to_int(realisateur) 
      acteur_1 = acteur_1.lower()
      acteur_1 = convert_to_int(acteur_1)
      acteur_2 = acteur_2.lower()
      acteur_2 = convert_to_int(acteur_2)
      genre = genre.lower()
      genre = convert_to_int(genre)
      prediction = model.predict([[genre, acteur_1, realisateur, acteur_2]])
      return prediction[0]/10

iface = gr.Interface(
  predict,
  [
        gr.inputs.Textbox(label="realisateur"),
        gr.inputs.Textbox(label="acteur 1"),
        gr.inputs.Textbox(label="acteur 2"),
        gr.inputs.Dropdown(["Adventure","Action", "Animation", "Biography", "Crime", "Comedy", "Drama", 
                            "Horror", "Family",  "Fantasy", "Music", "Mystery", "Romance", "Sci-Fi"],label="genre")
          
        
    ],
    gr.outputs.Textbox(label="Score")).launch()


if __name__ == "__main__":
    iface.launch()