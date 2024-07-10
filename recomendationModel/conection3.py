import sqlite3
import movies
import os
import uuid
import time

#create the database
database = sqlite3.connect('database/usersAndMovies')
cursor = database.cursor()

def createTables():
    query = """CREATE TABLE IF NOT EXISTS user (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(25) NOT NULL,
        password VARCHAR(45) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL);

        CREATE TABLE IF NOT EXISTS favorite_movies (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        movie_id VARCHAR(255) NOT NULL);

        CREATE TABLE IF NOT EXISTS wached_movies (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        movie_id VARCHAR(255) NOT NULL,
        rating INT NOT NULL)
        """
    cursor.executescript(query)

createTables()


def generate_id():
    return str(uuid.uuid4())

#create a user with a class
class createUser:
    def __init__(self, name, password, email=None):
        self.name = name
        self.password = password
        self.email = email
        self.id = generate_id()
        self.favoriteMovies = []
        self.wachedMovies = {}
    
    def addfavoriteMovies(self):
        moviesDict = movies.movies_title()
        print(f'Movies: {moviesDict}')
        print(f'Select your favorite movie by entering the movie name')

        favMovie = str(input('Write the movie name ')).title()
        try:
            if favMovie in moviesDict:
                self.favoriteMovies.append(moviesDict[favMovie]['id'])
                print(f'You have added {favMovie} to your favorite movies')
            else:
                print('Movie not found, try another page')
            print('add another movie? [Y/N]')
            choice = input("=>").lower()
            if choice == 'y':
                self.addfavoriteMovies()
            else:
                print('adding movies to Database...')
                time.sleep(1)
                print('Done')
        except Exception as e:
            print(f"error {e} has ocurred want to try again?[Y/N]")
            choice = input("=>").lower()
            if choice == 'y':
                self.addfavoriteMovies()
            else:
                time.sleep(0.3)
                print('done')

# add user to db
def addUser(user):
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE email = ?", (user.email,))
    userexistence = cursor.fetchone()[0]

    if userexistence > 0:
        print('email already used')
        return
    cursor.execute(f"INSERT INTO user (id, name, password, email) VALUES (?, ?, ?, ?)", (user.id, user.name, user.password, user.email))
    database.commit()
    print('user created succesful')

def addFavMovies(user):
    for i in (range(0, len(user.favoriteMovies))):
        cursor.execute(f"SELECT COUNT(*) FROM favorite_movies WHERE user_id = ? AND  movie_id = ?", (user.id, user.favoriteMovies[i]))
        relationexistence = cursor.fetchone()[0]
        if relationexistence > 0:
            print(f'movie with id {user.favoriteMovies[i]} already added')
            return 
        row_id = generate_id()
        cursor.execute(f"INSERT INTO favorite_movies (id, user_id, movie_id) VALUES (?, ?, ?)", (row_id, user.id, user.favoriteMovies[i]))
        database.commit()

# verify if movie id return the correct movie:
def allUserMovies(name, password, gmail):
    cursor.execute(f"SELECT name, movie_id FROM user LEFT JOIN favorite_movies as fav_mov ON user.id = fav_mov.user_id WHERE name = ? AND password = ? AND email = ?", (name, password, gmail))
    user = cursor.fetchone()
    if user is None:
        print('user not found')
        return
    movie = movies.searchMovie(user[1])
    return movie

print(allUserMovies('loco', 12345, 'elloco@gmail.com'))
database.close()
