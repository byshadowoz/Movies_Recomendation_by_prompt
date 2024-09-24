import sqlite3
import csv
import pandas as pd
import uuid
import ast


database = sqlite3.connect('database/usersAndMovie')
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
               id INT PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               adult INTEGER NOT NULL,
               original_language VARCHAR(255) NOT NULL,
               genres_ids INTEGER NOT NULL,
               popularity FLOAT NOT NULL,
               vote_average FLOAT NOT NULL,
               vote_count FLOAT NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS genres (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               animation INT NOT NULL,
               family INT NOT NULL,
               adventure INT NOT NULL,
               comedy INT NOT NULL,
               action INT NOT NULL,
               crime INT NOT NULL,
               thriller INT NOT NULL,
               science_fiction INT NOT NULL,
               drama INT NOT NULL,
               fantasy INT NOT NULL,
               horror INT NOT NULL,
               romance INT NOT NULL,
               war INT NOT NULL,
               music INT NOT NULL,
               western INT NOT NULL,
               TV_movie INT NOT NULL,
               mystery INT NOT NULL,
               history INT NOT NULL,
               documentary INT NOT NULL);""")

all_genres = ['Animation', 'Family', 'Adventure', 'Comedy', 'Action', 'Crime', 'Thriller', 
              'Science Fiction', 'Drama', 'Fantasy', 'Horror', 'Romance', 'War', 'Music', 
              'Western', 'TV Movie', 'Mystery', 'History', 'Documentary']

def insert_genres_and_movies():
    try:
        # Conectar a la base de datos
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
            # Leer el archivo CSV
            with open('allmovies.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Iterar sobre cada fila en el CSV
                for row in reader:
                    genres_list = ast.literal_eval(row['genre_ids'])  # Convertir la cadena en una lista

                    # Crear un diccionario con 0 para todos los géneros
                    genres_dict = {genre: 0 for genre in all_genres}

                    # Marcar con 1 los géneros presentes en la película
                    for genre in genres_list:
                        genre = genre.strip()
                        if genre in genres_dict:
                            genres_dict[genre] = 1

                    cursor.execute('''INSERT INTO genres (animation, family, adventure, comedy, action, crime, thriller, 
                                            science_fiction, drama, fantasy, horror, romance, war, music, 
                                            western, TV_movie, mystery, history, documentary)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (genres_dict['Animation'],
                          genres_dict['Family'],
                          genres_dict['Adventure'],
                          genres_dict['Comedy'],
                          genres_dict['Action'],
                          genres_dict['Crime'],
                          genres_dict['Thriller'],
                          genres_dict['Science Fiction'],
                          genres_dict['Drama'],
                          genres_dict['Fantasy'],
                          genres_dict['Horror'],
                          genres_dict['Romance'],
                          genres_dict['War'],
                          genres_dict['Music'],
                          genres_dict['Western'],
                          genres_dict['TV Movie'],
                          genres_dict['Mystery'],
                          genres_dict['History'],
                          genres_dict['Documentary']))

                    # Generar un UUID único
                    movie_id = str(uuid.uuid4())

                    # Insertar en la tabla movies
                    cursor.execute('''
                        INSERT INTO movies(id, title, adult, original_language, genres_ids, popularity, 
                                            vote_average, vote_count)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (movie_id, 
                          row['title'], 
                          row['adult'], 
                          row['original_language'], 
                          ','.join(genres_list),  # Usar los géneros originales en lugar de los diccionarios
                          row['popularity'], 
                          row['vote_average'], 
                          row['vote_count']))

            # Confirmar cambios
            conn.commit()
            
    except sqlite3.Error as e:
        print(f"Error: {e}")

insert_genres_and_movies()
database.close()