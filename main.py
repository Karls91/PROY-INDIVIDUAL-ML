import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import pandas as pd
import uvicorn
from fastapi.templating import Jinja2Templates


app = FastAPI()

from fastapi import HTTPException

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "message": f"Error HTTP: {exc}"})


templates = Jinja2Templates(directory="templates")

#1
@app.get("/PlayTimeGenre/{genero}", response_class=HTMLResponse)
async def PlayTimeGenre(request: Request, genero: str):
    # Leemos el archivo CSV
    genre_df = pd.read_csv("/data/play_time_genre.csv")

    # Se convierte el género ingresado a minúsculas para hacer la comparación sin importar la capitalización
    genero = genero.lower()

    # Se filtra el DataFrame por el género indicado (en minúsculas)
    genre_df = genre_df[genre_df['genres'].str.lower() == genero]

    if genre_df.empty:
        message = f"No hay datos para el género {genero}."
        return templates.TemplateResponse("error.html", {"request": request, "message": message})

    # Se realiza una agrupación por año y se suman las horas playtime
    grouped_df = genre_df.groupby('release_date')['playtime_forever'].sum()

    # Se realiza una búsqueda para el año con más horas jugadas
    max_year = grouped_df.idxmax()

    # Convertir max_year a un tipo de dato nativo de Python
    max_year = int(max_year)

    return templates.TemplateResponse("playtime_genre.html", {"request": request, "genero": genero, "max_year": max_year})


#2
@app.get("/UserForGenre/{genero}", response_class=HTMLResponse)
async def UserForGenre(request: Request, genero: str):
    # Leemos el archivo CSV
    df_filtered = pd.read_csv("/data/df_user_genre.csv")

    # Filtramos el DataFrame por el género dado
    df_filtered = df_filtered[df_filtered['genres'].str.lower() == genero.lower()]

    if df_filtered.empty:
        message = f"No hay datos para el género {genero}."
        return templates.TemplateResponse("error.html", {"request": request, "message": message})

    # Se busca el usuario con más horas jugadas
    usuario_max_horas = df_filtered.loc[df_filtered['playtime_forever'].idxmax()]['user_id']

    # Se crea una lista de acumulación de horas jugadas por año
    acumulacion_por_ano = df_filtered.groupby(df_filtered['release_date'].astype(int).astype(str).str[:4])[
        'playtime_forever'].sum().reset_index()
    horas_por_ano = [{"Año": int(row['release_date']), "Horas": row['playtime_forever']} for index, row in
                     acumulacion_por_ano.iterrows()]

    # Se crea el diccionario de retorno
    resultado = {
        "Usuario con más horas jugadas para Género ": usuario_max_horas,
        "Horas jugadas": horas_por_ano}

    return templates.TemplateResponse("user_for_genre.html", {"request": request, "genero": genero, "resultado": resultado})


#3
@app.get("/UsersRecommend/{year}", response_class=HTMLResponse)
async def UsersRecommend(request: Request, year: int):
    # Leemos el archivo CSV
    df_users_recommend = pd.read_csv("/data/df_users_recommend.csv")

    # Se realiza un filtrado por año
    df_filtered = df_users_recommend[df_users_recommend['release_date'] == year]

    # Se filtran las recomendaciones positivas/neutrales
    df_filtered = df_filtered[df_filtered['sentiment_analysis'].isin([1, 2])]

    # Se realiza una agrupación por título y con las recomendaciones
    game_recommendations = df_filtered.groupby('title')['sentiment_analysis'].count()

    # Se ordenan de mayor a menor y se toman los 3 primeros
    top_3_recommendations = game_recommendations.sort_values(ascending=False).head(3)

    # Se crea una lista con los resultados
    result_list = [{"Puesto {}: {}".format(i + 1, game): count} for i, (game, count) in enumerate(top_3_recommendations.items())]

    return templates.TemplateResponse("users_recommend.html", {"request": request, "year": year, "result_list": result_list})


#4
@app.get("/UsersWorstDeveloper/{year}", response_class=HTMLResponse)
async def UsersWorstDeveloper(request: Request, year: int):
    # Leemos el archivo CSV
    df_worst_dev = pd.read_csv("/data/df_worst_dev.csv")

    # Filtrar por año
    df_filtered = df_worst_dev[df_worst_dev['release_date'] == year]

    # Filtrar por recomendaciones negativas
    df_filtered = df_filtered[df_filtered['sentiment_analysis'] == 0]
 # Contar la cantidad de juegos no recomendados por cada desarrolladora
    worst_dev_counts = df_filtered['developer'].value_counts()

    # Tomar las 3 desarrolladoras con menos juegos recomendados
    worst_dev_top_3 = worst_dev_counts.tail(3)

    # Crear la lista de resultados
    result_list = [{"Puesto {}: {}".format(i + 1, dev): count} for i, (dev, count) in enumerate(worst_dev_top_3.items())]

    return templates.TemplateResponse("worst_developer.html", {"request": request, "year": year, "result_list": result_list})


#5
@app.get("/sentiment_analysis/{developer}", response_class=HTMLResponse)
async def sentiment_analysis(request: Request, developer: str):
    # Leemos el archivo CSV
    df_sentiment = pd.read_csv("/data/df_sentiment.csv")

    # Convertimos a minúsculas tanto el nombre del desarrollador en el DataFrame como el proporcionado por el usuario
    df_sentiment['developer_lower'] = df_sentiment['developer'].str.lower()
    developer_lower = developer.lower()

    # Se filtra el DataFrame para obtener solo las filas que corresponden al desarrollador
    df_developer = df_sentiment[df_sentiment['developer_lower'] == developer_lower]

    # Se cuentan la cantidad de registros de cada categoría de sentiment_analysis
    sentiment_counts = df_developer['sentiment_analysis'].value_counts().to_dict()

    # Se crea el diccionario retorno
    result_dict = {developer: sentiment_counts}

    return templates.TemplateResponse("sentiment_analysis.html", {"request": request, "developer": developer, "result_dict": result_dict})


# Inicio del servidor FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


