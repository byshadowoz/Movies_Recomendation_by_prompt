import movies
import genres


class userdata:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.favoriteMovies = []
        self.wachedMovies = {}

    def addFavoriteMovies(self):
        moviesDict = movies.movies_id()
        print(f'Movies: {moviesDict}')
        print('Select your favorite movie/s by entering the movie id')

        favMovies = int(input('Select your favorite movie/s '))
        try:
            while True:
                if favMovies in moviesDict:
                    self.favoriteMovies.append(favMovies)
                    print(self.favoriteMovies)
                    print('stop? [Y/N]')
                    choice = input()
                    if choice.lower() == 'y':
                        return
                    else:
                        self.addFavoriteMovies()
                else:
                    print('Invalid id, try again')
                    self.addFavoriteMovies()

        except Exception as e:
            print(f'Error: {e}')
            print('want to continue? [Y/N]?')
            choice = input()
            if choice.lower() == 'y':
                self.addFavoriteMovies()
            else:
                return
    def addWachedMovies(self):
        moviesDict = movies.movies_id()
        print(f'Movies: {moviesDict}')
        print('Select your wached movie by entering the movie id')
        wachedMovies = int(input('Select your wached movie '))
        try:
            while True:
                if wachedMovies in moviesDict:
                    print('how much do you like de movie? 1/10')
                    rating = float(input())
                    self.wachedMovies[wachedMovies] = rating

                    print('Add more?? [Y/N]')
                    choice = input()
                    if choice.lower() == 'y':
                        self.addWachedMovies()
                    else:
                        return 
                else:
                    print('Invalid id, try again')
                    self.addWachedMovies()
        except Exception as e:
            print(f'Error: {e}')
            print('want to continue? [Y/N]?')
            choice = input()
            if choice.lower() == 'y':
                self.addWachedMovies()
            else:
                return




    def recomendMovie(self):
        # TODO: recommendation logic goes here
        pass