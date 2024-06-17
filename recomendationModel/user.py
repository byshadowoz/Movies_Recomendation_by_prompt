import requests
import movies
import genres

class createUser:
    def __init__(self):
        self.favoriteMovies = {}

    def addFavoriteMovies(self):
        moviesDict = movies.movies_id()
        print(f'Movies: {moviesDict.values()}')
        print('Select your favorite movie/s by entering the movie id')

        favMovies = int(input('Select your favorite movie/s '))
        try:
            while True:
                if favMovies in moviesDict:
                    self.favoriteMovies = self.favoriteMovies[moviesDict[favMovies]] = favMovies
                    print('stop? [Y/N]')
                    choice = input()
                    if choice.lower() == 'y':
                        return 
                    else:
                        favMovies = int(input('Select your next favorite movie/s '))
                else:
                    print('Invalid id, try again')
                    favMovies = int(input('Select your favorite movie/s '))

        except Exception as e:
            print(f'Error: {e}')
            print('want to continue? [Y/N]?')
            choice = input()
            if choice.lower() == 'y':
                self.addFavoriteMovies()
            else:
                return
    
    def seeFavoriteMovies(self):
        print(f'Favorite movies for {self.name}:')
        for movie, id in self.favoriteMovies.items():
            print(f'{movie} with id: {id}')
    
    def recomendMovie(self):
        # recommendation logic goes here
        pass

user = createUser()
user.addFavoriteMovies()
print(user.favoriteMovies)

    



