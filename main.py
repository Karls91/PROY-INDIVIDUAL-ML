import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import pandas as pd
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ruta del directorio actual del script
current_directory = os.path.dirname(os.path.realpath(__file__))

#1<<
@app.get("/PlayTimeGenre/{genero}", response_class=HTMLResponse)
async def PlayTimeGenre(request: Request, genero: str):
    # Combinamos la ruta del directorio actual con la ruta relativa del archivo CSV
    csv_path = os.path.join(current_directory, "data", "play_time_genre.csv")

    # Leemos el archivo CSV
    genre_df = pd.read_csv(csv_path)

    # Se convierte el género ingresado a minúsculas para hacer la comparación sin importar la capitalización
    genero = genero.lower()

    # Se filtra el DataFrame por el género indicado (en minúsculas)
    genre_df = genre_df[genre_df['genres'].str.lower() == genero]

    if genre_df.empty:
        return templates.TemplateResponse("no_data.html", {"request": request, "genero": genero})

    # Se realiza una agrupación por año y se suman las horas playtime
    grouped_df = genre_df.groupby('release_date')['playtime_forever'].sum()

    # Se realiza una búsqueda para el año con más horas jugadas
    max_year = grouped_df.idxmax()

    # Convertir max_year a un tipo de dato nativo de Python
    max_year = int(max_year)

    return templates.TemplateResponse("playtime_genre.html", {"request": request, "genero": genero, "max_year": max_year})


#2<<
@app.get("/UserForGenre/{genero}", response_class=HTMLResponse)
async def UserForGenre(request: Request, genero: str):
    # Combinamos la ruta del directorio actual con la ruta relativa del archivo CSV
    csv_path = os.path.join(current_directory, "data", "df_user_genre.csv")

    # Leemos el archivo CSV
    df_filtered = pd.read_csv(csv_path)

    # Filtramos el DataFrame por el género dado
    df_filtered = df_filtered[df_filtered['genres'].str.lower() == genero.lower()]

    if df_filtered.empty:
        return templates.TemplateResponse("no_data.html", {"request": request, "genero": genero})

    # Se busca el usuario con más horas jugadas
    usuario_max_horas = df_filtered.loc[df_filtered['playtime_forever'].idxmax()]['user_id']

    # Se crea una lista de acumulación de horas jugadas por año
    acumulacion_por_ano = df_filtered.groupby(df_filtered['release_date'].astype(int).astype(str).str[:4])['playtime_forever'].sum().reset_index()
    horas_por_ano = [{"Año": int(row['release_date']), "Horas": row['playtime_forever']} for index, row in acumulacion_por_ano.iterrows()]

    # Se crea el diccionario de retorno
    resultado = {
        "Usuario con más horas jugadas para Género ": usuario_max_horas,
        "Horas jugadas": horas_por_ano
    }

    return templates.TemplateResponse("user_for_genre.html", {"request": request, "genero": genero, "resultado": resultado})


#3<<
@app.get("/UsersRecommend/{year}", response_class=HTMLResponse)
async def UsersRecommend(request: Request, year: int):
    # Combinamos la ruta del directorio actual con la ruta relativa del archivo CSV
    csv_path = os.path.join(current_directory, "data", "df_users_recommend.csv")

    # Leemos el archivo CSV
    df_users_recommend = pd.read_csv(csv_path)

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


#4<<
@app.get("/UsersWorstDeveloper/{year}", response_class=HTMLResponse)
async def UsersWorstDeveloper(request: Request, year: int):
    # Combin


