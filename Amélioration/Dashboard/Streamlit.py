import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

st.title("Tableau de bord IMDb")
st.write("""Exploration de la base de donnée""")

df = pd.read_csv("/Users/manon/Projet/Projet-SIMPLON/Amélioration/Data/movies2.csv", encoding="latin-1")

def load_data(nrows):
    df = pd.read_csv("/Users/manon/Projet/Projet-SIMPLON/Amélioration/Data/movies2.csv", encoding="latin-1", nrows=nrows)
    df = df.rename(columns={'11:14': 'film', '7.2': 'metascore', 'Crime': 'genre', 'Greg Marcks': 'realisateur',
                                'Henry Thomas': 'acteur_1', 'Colin Hanks': 'acteur_2', '6000000': 'budget',
                                '0': 'votes2', '0.1': 'vote', 'Aug 12, 2005': 'date'})
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df = df.set_index(['date'])
    return df


data_load_state = st.text('Chargement en cours...')
data = load_data(10000)
st.dataframe(data)
data_load_state.text('Chargement terminé!')

st.subheader('Nombre de films par genre')
fig, ax = plt.subplots()
data['genre'].value_counts().plot.bar(ylim=0)
st.pyplot(fig)