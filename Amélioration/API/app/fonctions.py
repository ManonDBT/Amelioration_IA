import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer, util
import math

model = SentenceTransformer('paraphrase-distilroberta-base-v1', device="cuda")

imdb_movies = pd.read_json('/Users/manon/Projet/Projet-SIMPLON/Amélioration/imdb.json', orient='split')



## Dropping off rows where Movie Description is NULL
imdb_movies = imdb_movies[pd.notnull(imdb_movies['description'])]
imdb_movies = imdb_movies.reset_index(drop=True)

imdb_movies['id'] = imdb_movies.index



sentences = imdb_movies['description'].tolist()


embeddings = model.encode(sentences)
faiss.normalize_L2(embeddings)



dim = 768
ncentroids = 50
m = 16
quantiser = faiss.IndexFlatL2(dim)
index = faiss.IndexIVFPQ(quantiser, dim, ncentroids, m, 8)
index.train(embeddings)
print(index.is_trained)
faiss.write_index(index, "trained.index")

ids = imdb_movies['id'].tolist()
ids = np.array(ids)
index.add_with_ids(embeddings, ids)
print(index.ntotal)

faiss.write_index(index, "block.index")


def searchFAISSIndex(data, id_col_name, query, index, nprobe, model, topk=20):
    query_embedding = model.encode([query])[0]
    dim = query_embedding.shape[0]
    query_embedding = query_embedding.reshape(1, dim)
    faiss.normalize_L2(query_embedding)

    index.nprobe = nprobe

    D, I = index.search(query_embedding, topk)
    ids = [i for i in I][0]
    L2_score = [d for d in D][0]
    inner_product = [calculateInnerProduct(l2) for l2 in L2_score]
    search_result = pd.DataFrame()
    search_result[id_col_name] = ids
    search_result['cosine_sim'] = inner_product
    search_result['L2_score'] = L2_score
    dat = data[data[id_col_name].isin(ids)]
    dat = pd.merge(dat, search_result, on=id_col_name)
    dat = dat.sort_values('cosine_sim', ascending=False)
    return dat


def calculateInnerProduct(L2_score):
    return (2 - math.pow(L2_score, 2)) / 2

query="Princess in castle"
search_result=searchFAISSIndex(imdb_movies,"id",query,index,nprobe=10,model=model,topk=20)
search_result=search_result[['id','description','titre','cosine_sim','L2_score']]

search_result