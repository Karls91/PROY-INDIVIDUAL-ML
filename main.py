from typing import Union
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

#1<<
@app.get("/PlayTimeGenre/{genero}")
async def PlayTimeGenre(genero: str):
    # Leemos el archivo parquet
    genre_df = pd.read_csv("data/play_time_genre.csv")

def PlayTimeGenre(genero: str):
    # Se filtra el DataFrame por el género indicado
    genre_df = play_time_genre[play_time_genre['genres'] == genero]

    if genre_df.empty:
        return f"No hay datos para el género {genero}."

    # Se realiza una agrupación por año y se suman las horas playtime
    grouped_df = genre_df.groupby('release_date')['playtime_forever'].sum()

    # Se realiza una búsqueda para el año con más horas jugadas
    max_year = grouped_df.idxmax()

    return {f"Año de lanzamiento con más horas jugadas para el género {genero}": max_year}



#2<<
@app.get("/UserForGenre/{genero}")
async def UserForGenre(genero: str):
     # Leemos el archivo parquet
    df_filtered = pd.read_csv("/data/df_user_genre.csv")
    
    # Filtramos el DataFrame por el género dado
    df_filtered = df_user_genre[df_user_genre['genres'].str.lower() == genero.lower()]

    if df_filtered.empty:
        return {"Mensaje": f"No hay datos para el género {genero}."}

    # Se busca el usuario con más horas jugadas
    usuario_max_horas = df_filtered.loc[df_filtered['playtime_forever'].idxmax()]['user_id']

    # Se crear una lista de acumulación de horas jugadas por año
    acumulacion_por_ano = df_filtered.groupby(df_filtered['release_date'].astype(int).astype(str).str[:4])['playtime_forever'].sum().reset_index()
    horas_por_ano = [{"Año": int(row['release_date']), "Horas": row['playtime_forever']} for index, row in acumulacion_por_ano.iterrows()]

    # Se crear el diccionario de retorno
    resultado = {
        "Usuario con más horas jugadas para Género ": usuario_max_horas,
        "Horas jugadas": horas_por_ano
    }

    return resultado


#3<<
@app.get("/UsersRecommend/{year}")
async  def UsersRecommend(df_users_recommend, año):
    
      # Leemos el archivo csv
    df_filtered = pd.read_csv("/data/df_users_recommend.csv")
    # Se realiza un filtrado por año
   
    df_filtered = df_users_recommend[df_users_recommend['release_date'] == año]

    # Se filtran las recomendaciones positivas/neutrales
    df_filtered = df_filtered[df_filtered['sentiment_analysis'].isin([1, 2])]

    # Se realiza una agrupación por título y con las recomendaciones
    game_recommendations = df_filtered.groupby('title')['sentiment_analysis'].count()

    # Se ordenan de mayor a menor y se tomar los 3 primeros
    top_3_recommendations = game_recommendations.sort_values(ascending=False).head(3)

    # Se crea una la lista con los resultados
    result_list = [{"Puesto {}: {}".format(i + 1, game): count} for i, (game, count) in enumerate(top_3_recommendations.items())]

    return result_list


#4<<
@app.get("/UsersWorstDeveloper/{year}")
async def UsersWorstDeveloper(df_worst_dev, año):
    
      # Leemos el archivo csv
    df_filtered = pd.read_csv("/data/df_worst_dev.csv")
    # Filtrar por año
    df_filtered = df_worst_dev[df_worst_dev['release_date'] == año]

    # Filtrar por recomendaciones negativas
    df_filtered = df_filtered[df_filtered['sentiment_analysis'] == 0]

    # Contar la cantidad de juegos no recomendados por cada desarrolladora
    worst_dev_counts = df_filtered['developer'].value_counts()

    # Tomar las 3 desarrolladoras con menos juegos recomendados
    worst_dev_top_3 = worst_dev_counts.tail(3)

    # Crear la lista de resultados
    result_list = [{"Puesto {}: {}".format(i + 1, dev): count} for i, (dev, count) in enumerate(worst_dev_top_3.items())]

    return result_list



#5<<
@app.get("/sentiment_analysis/{empresa_desarrolladora}")
async def sentiment_analysis(developer):
    df_empresa = pd.read_csv("/data/df_sentiment.csv")
    
    # Se filtra el DataFrame para obtener solo las filas que corresponden al developer
    df_empresa = df_sentiment[df_sentiment['developer'] == developer]
    
    # Se cuentan la cantidad de registros de cada categoría de sentiment_analysis
    sentiment_counts = df_empresa['sentiment_analysis'].value_counts().to_dict()
    
    # Se crea el diccionario retorno
    result_dict = {developer: sentiment_counts}
    
    return result_dict


