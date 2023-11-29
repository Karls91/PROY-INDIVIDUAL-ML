<H1 align="center">Proyecto de recomendaciones de videojuegos para la plataforma Steam</H1>


Este constituye el desarrollo inicial de mi primer proyecto individual durante la etapa de laboratorios del bootcamp 'Data Scientist' de Henry. En este proyecto, se nos solicita la tarea de crear un modelo de Machine Learning que abarcara desde la recolección y tratamiento de datos hasta el entrenamiento y mantenimiento continuo del modelo para adaptarse a nuevos datos.


## Marco de Referencia
Steam, la plataforma multinacional de distribución digital de videojuegos desarrollada por Valve Corporation en 2003, inicialmente concebida para proporcionar actualizaciones automáticas a los juegos de Valve, se ha expandido para incluir juegos de terceros. En esta ocasión, Steam busca abordar un desafío de negocio desarrollando un sistema de recomendación de videojuegos para sus usuarios.

Se nos ha solicitado la entrega rápida de un Producto Mínimo Viable (MVP), que se basa en el desarrollo de una Interfaz de Programación de Aplicaciones (API). Esto permitirá la accesibilidad a los datos de la empresa para realizar consultas necesarias, junto con la implementación de un sistema de recomendación de videojuegos. 


## Fuentes de datos

Se nos proporcionaron 3 archivos json y un diccionario de datos, a los cuales debimos realizar diferentes procesos de ETL para dejarlos preparados para nuestro futuro modelo.

[link](https://drive.google.com/drive/folders/18ubpDrUfChnage6gRNDTu68SxJlr4_xZ?usp=drive_link).


## Transformaciones (ETL) y EDA

Se realizaron las transformaciones de cada dataset por separado para un mejor entendimiento de los datos:
[link]https://github.com/Karls91/PROY-INDIVIDUAL-ML/blob/main/ETL/Items.ipynb   Transformaciónes dataset "australian_users_items"
[link]https://github.com/Karls91/PROY-INDIVIDUAL-ML/blob/main/ETL/Reviews.ipynb Transformaciónes dataset "australian_users_reviews"
[link]https://github.com/Karls91/PROY-INDIVIDUAL-ML/blob/main/ETL/games.ipynb   Transformaciónes dataset "output_steam_games"


## Desarrollo de FastAPI

Se proponen las siguientes funciones para los endpoints que se consumirán en la API:

ef PlayTimeGenre(genero:str) Ingresando el nombre de un genero, devuelve el año con dcon mas horas jugadas para dicho género. Para esto, se decide utilizar directamente el dataset proporcionado, luego de haber pasado por el EDA y el ETL, pero quedandonos únicamente con la información relevante. 

def UserForGenre( genero : str ): Ingresando un género, devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento. Para esto necesitamos hacer un merge entre los datasets 'steam_games' y 'user_items' a través del id del item, ya que encontramos la siguiente información por dataset:

def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)

def UsersWorstDeveloper( año : int ) Ingresando un año, devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 

def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.

## Deployment
Se realiza el deployment en la plataforma de Render para disponibilizar las consultas a cualquier persona con internet. A continuación se encuentra el link a Render: [link]https://juan-contreras.onrender.com/docs

Funciones realizadas: [Link]https://github.com/Karls91/PROY-INDIVIDUAL-ML/blob/main/endpoints.ipynb

## Video: https://drive.google.com/drive/folders/1np69iiXHDf-tcMXtKyQjKysgQcPLmPDM?usp=sharing


