from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


  
st.title("Dashboard IMDb")
st.sidebar.title("Sélectionner des graphiques visuels")
st.sidebar.markdown("Sélectionnez les graphiques / graphiques en conséquence:")
  
data = pd.read_csv("./IMDb movies.csv", sep=";")

country_df =  data[['title','country']].groupby(['country']).count().reset_index().rename(columns={'title':'nombre'})
country_df = country_df.sort_values(by=['nombre'], ascending=False)

genres_df = data[['genre','title', 'year']].groupby(['genre', 'year']).count().reset_index().rename(columns={'title':'nombre'})
genres_df = genres_df.sort_values(by='nombre', ascending=False)

year_df = data[['year','title']].groupby(['year']).count().reset_index().rename(columns={'title':'nombre'})

  
chart_visual = st.sidebar.selectbox('Select Charts/Plot type', 
                                    ('Line Chart', 'Bar Chart', 'Bubble Chart'))
  
st.sidebar.checkbox("Afficher l'analyse par année ", True, key = 1)
selected_status = st.sidebar.selectbox('Selectionne une option',
                                       options = ['pays', 'genre', 'année', 'score'])
  
  
  
fig = go.Figure()


  
if chart_visual == 'Line Chart':
    if selected_status == 'pays':
        fig.add_trace(go.Scatter(x = country_df.country.unique(), y = country_df.nombre,
                                 mode = 'lines',
                                 name = 'Nombre de film par année'))
    if selected_status == 'genre':
        fig.add_trace(go.Scatter(x = genres_df.genre.unique(), y = genres_df.nombre,
                                 mode = 'lines',
                                 name = 'Nombre de film par genre'))
                      
    if selected_status == 'année':
        fig.add_trace(go.Scatter(x = year_df.year.unique(), y = year_df.nombre,
                                 mode = 'lines',
                                 name = 'Nombre de film par année'))
    
    
  
elif chart_visual == 'Bar Chart':
    if selected_status == 'année':
         fig.add_trace(go.Bar(x=genres_df.year.unique(), y=genres_df.nombre,
                             name='Genre de film par année'))
         
    if selected_status == 'Smoked':
        fig.add_trace(go.Bar(x=data.Country, y=data.Smokes,
                             name='Smoked'))
    if selected_status == 'Never_Smoked':
        fig.add_trace(go.Bar(x=data.Country, y=data.Never_Smoked,
                             name='Never_Smoked'))
    if selected_status == 'Unknown':
        fig.add_trace(go.Bar(x=data.Country, y=data.Unknown,
                             name="Unknown"))
  

  
st.plotly_chart(fig, use_container_width=True)


# @st.cache
# def load_data():
#    movies = Path() / './IMDb movies.csv'
#    data = pd.read_csv(movies, sep=';')
#    return data

# df = load_data()
# st.write(df)