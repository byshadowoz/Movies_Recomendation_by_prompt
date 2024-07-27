import sqlite3
import movies as mvs
import uuid
import time

#create the database
database = sqlite3.connect('database/usersAndMovies')
cursor = database.cursor()

def createTables():
    query = """CREATE TABLE IF NOT EXISTS user (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL);

        CREATE TABLE IF NOT EXISTS favorite_movies (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        movie_id VARCHAR(255) NOT NULL);

        CREATE TABLE IF NOT EXISTS wached_movies (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        movie_id VARCHAR(255) NOT NULL,
        rating DECIMAL NOT NULL);
        """
    cursor.executescript(query)

createTables()


def generate_id():
    return str(uuid.uuid4())
idx = str(generate_id())
#create a user

# add user to db
def addUser(username, email, password):
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE email = ?",
                    (email,))
    userexistence = cursor.fetchone()[0]
    if userexistence > 0:
        print('email already used')
        return
    
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE name = ?",
                    (username,))
    userexistence = cursor.fetchone()[0]
    if userexistence > 0:
        print('username already used')
        return
    
    cursor.execute(f"INSERT INTO user (id, name, password, email) VALUES (?, ?, ?, ?)",
                    (idx, username, password, email))
    database.commit()
    print('user created succesful')

def addfavoriteMovies(username, password):
    # check if user exist
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE  name = ? AND  password = ?", (username, password))
    userexistence = cursor.fetchone()[0]
    if userexistence == 0:
        print('user not found')
        return
    
    favoriteMovies = []  
    moviesDict = mvs.movies_title()
    print(f'Movies: {moviesDict}')
    print(f'Select your favorite movie by entering the movie name')

    favMovie = str(input('Write the movie name ')).title()
    try:
        if favMovie in moviesDict:
            favoriteMovies.append(moviesDict[favMovie]['id'])
            print(f'You have added {favMovie} to your favorite movies')
        else:
            print('Movie not found, try another page')
        print('add another movie? [Y/N]')
        choice = input("=>").lower()
        if choice == 'y':
            addfavoriteMovies(username, password)
        else:
            print('adding movies to Database...')
            time.sleep(1)

            print('Done')
    except Exception as e:
        print(f"error {e} has ocurred want to try again?[Y/N]")
        choice = input("=>").lower()
        if choice == 'y':
            addfavoriteMovies(username, password)
        else:
            time.sleep(0.3)
            print('done')
    _addFavMoviesToDb(username, password, favoriteMovies)

def _addFavMoviesToDb(username, password, favoriteMovies):
    # check if favoriteMovies is empty
    if len(favoriteMovies) < 1:
        print('no favorite movies')
        return
    # search user_id
    cursor.execute(f"SELECT id FROM user WHERE  name = ? AND  password = ?", (username, password))
    user_id = cursor.fetchone()[0]
    for i in (range(0, len(favoriteMovies))):
        cursor.execute(f"SELECT COUNT(*) FROM favorite_movies WHERE user_id = ? AND  movie_id = ?",
                        (user_id, favoriteMovies[i]))
        relationexistence = cursor.fetchone()[0]
        if relationexistence > 0:
            print(f'movie with id {favoriteMovies[i]} already added')
            return 
        row_id = generate_id()
        cursor.execute(f"INSERT INTO favorite_movies (id, user_id, movie_id) VALUES (?, ?, ?)",
                        (row_id, user_id, favoriteMovies[i]))
        database.commit()

def allUserMovies(name, password, dbTable):
    cursor.execute(f"SELECT movie_id FROM user LEFT JOIN favorite_movies as fav_mov ON user.id = fav_mov.user_id WHERE name = ? AND password = ?",
                    (name, password))
    user = cursor.fetchall()
    if user is None:
        print('user not found, try check if the username or the password is correct')
        return
    moviesTable = []
    if dbTable == 'f':
        for movie_id in user:
            moviesTable.append(mvs.searchMovie(movie_id[0]))
        moviesTable
        return moviesTable
    elif dbTable == 'w':
        cursor.execute(f"SELECT movie_id FROM user LEFT JOIN wached_movies as whcd_mov ON user.id = whcd_mov.user_id WHERE name = ? AND password = ?",
                        (name, password))
        user = cursor.fetchall()    
        if user is None:
            print('user not found')
            return
        for movie_id in user:
            moviesTable.append(mvs.searchMovie(movie_id[0]))
        moviesTable
        return moviesTable
    else:
        print('invalid choice')
        return
        
    
def addWachedMovies(username, password):
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE  name = ? AND  password = ?", (username, password))
    userexistence = cursor.fetchone()[0]
    if userexistence == 0:
        print('user not found')
        return
    
    moviesDict = mvs.movies_title()

    cursor.execute(f"SELECT id FROM user WHERE  name = ? AND  password = ?", (username, password))
    user_id = cursor.fetchone()[0]

    print(f'Movies: {moviesDict}')
    print(f'Select the wached movie by entering the movie name')

    wachedMovie = str(input('Write the movie name ')).title()
    try:
        if wachedMovie in moviesDict:
            ratingg = None
            while ratingg is None:
                ratingg = int(input('Write the rating of the movie [1/10] '))
                if ratingg < 1 or ratingg > 10:
                    print('The rating must be between 1 and 10')
                    ratingg = None

            cursor.execute(f"INSERT INTO wached_movies (id, user_id, movie_id, rating) VALUES (?, ?, ?, ?)",
                            (generate_id(), user_id, moviesDict[wachedMovie]['id'], ratingg))
            database.commit()
            print(f"You rated the movie {ratingg} out of 10.")
            print('add another movie? [Y/N]')
            if str(input()).lower() == 'y':
                addWachedMovies(username, password)
            else:
                return
        else:
            print('movie not found, try again')
            addWachedMovies(username, password)
    except Exception as e:
        print(f'error: {e} has ocurred want try again? [Y/N]?')
        if str(input('-> ')).lower() == 'y':
            addWachedMovies(username, password)
        else:
            return
