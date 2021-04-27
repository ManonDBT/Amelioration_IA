import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer, util
import math
from fastapi import FastAPI
from app import fonctions

app = FastAPI()

model = SentenceTransformer('paraphrase-distilroberta-base-v1', device="cuda")


def search_result() :
	description = input()
	search_result = searchFAISSIndex(imdb_movies, "id", description, index, nprobe=10, model=model, topk=20)
	search_result = search_result[['id', 'description', 'titre', 'cosine_sim', 'L2_score']]
	return search_result


@app.get('/')
def get_root():

	return {'message': 'Bienvenue sur la recommandation de film API'}

@app.get('/recommandation/')
async def detect_spam_query(message: str):
	return classify_message(model, message)

@app.get('/recommandation/{message}')
async def detect_spam_path(message: str):
	return classify_message(model, message)