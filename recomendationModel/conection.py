import mysql.connector
import dotenv
import os 
import uuid
import createUser as us

def generate_uuid():
  return uuid.uuid4()

dotenv.load_dotenv()

database = mysql.connector.connect(user=os.environ.get('user'), password=os.environ.get('password'),
                                    host='localhost',
                                    port = '3306',
                                    database='moviesusersdb')

cursor = database.cursor()

# Create database
sql = 'CREATE DATABASE IF NOT EXISTS moviesusersdb'
cursor.execute(sql)

userTable = """CREATE TABLE IF NOT EXISTS USER (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    password VARCHAR(45) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL)
    )"""

favorite_movies = """CREATE TABLE IF NOT EXISTS FAVORITE_MOVIES (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    movie_id VARCHAR(255) NOT NULL)"""

wached_movies = """CREATE TABLE IF NOT EXISTS WACHED_MOVIES (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    movie_id VARCHAR(255) NOT NULL,
    rating INT NOT NULL)"""

cursor.execute(userTable)
cursor.execute(favorite_movies)
cursor.execute(wached_movies)

class createduser:
        name = str(input('Username '))
        password = str(input('Password '))
        try:
            user_id = str(uuid.uuid4())
            # hashed_password = hash_password(password)  # Replace with secure password hashing

            new_user = """INSERT INTO USER (id, name, password) VALUES (%s, %s, %s)"""
            val = (user_id, name, password)
            cursor.execute(new_user, val)

            user = us.userdata(user_id, name, password)  # Pass generated ID and hashed password
            print('Add a favorite Movie? [Y/N]')
            answer = input()
            if answer.lower() == 'y':
                user.addFavoriteMovies()

                for movie in user.favoriteMovies:
                    uni_id = str(generate_uuid())
                    movie_id = str(movie)
                    val = (uni_id, user_id, movie_id)
                    sql = """
                    INSERT INTO FAVORITE_MOVIES (id, user_id, movie_id) VALUES (%s, %s, %s)
                    """
                    cursor.execute(sql, val)

            print('Add a watched Movie? [Y/N]')
            answer2 = input()
            if answer2.lower() == 'y':
                user.addWachedMovies()

                for movie, rating in user.wachedMovies.items():
                    uni_id = str(generate_uuid())
                    movie_id = str(movie)
                    val = (uni_id, user_id, movie_id, rating)
                    sql = """INSER INTO WACHED_MOVIES (id, user_id, movie_id, rating) VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, val)

            database.commit()  # Commit changes to the database
        except Exception as e:
            print("Error creating user:", e)

#Disconnecting from the db
database.close()

user = {
    'id': 'user_id',
    'name': 'name',
    'password': 'password',
    'favoriteMovies': ['movie1', 'movie2', 'movie3'],
    'wachedMovies': {'movie1': 5, 'movie2': 4,}
}