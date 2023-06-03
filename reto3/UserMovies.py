from mrjob.job import MRJob

class MRUserMovies(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield user, (movie, float(rating))

    def reducer(self, user, movie_rating_pairs):
        num_movies = 0
        total_rating = 0
        for movie, rating in movie_rating_pairs:
            num_movies += 1
            total_rating += rating
        yield user, (num_movies, total_rating / num_movies)

if __name__ == '__main__':
    MRUserMovies.run()
