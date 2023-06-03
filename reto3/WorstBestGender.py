from mrjob.job import MRJob
from mrjob.step import MRStep

class MRBestWorstMovieByGenre(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield (genre, movie), float(rating)

    def reducer(self, keys, ratings):
        ratings_list = list(ratings)
        if ratings_list:
            avg_rating = sum(ratings_list) / len(ratings_list)
            yield keys[0], (keys[1], avg_rating)

    def reducer_find_best_worst(self, genre, movie_avg_ratings):
        best_movie = max(movie_avg_ratings, key=lambda x: x[1])
        worst_movie = min(movie_avg_ratings, key=lambda x: x[1])
        yield genre, (best_movie, worst_movie)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_best_worst)
        ]

if __name__ == '__main__':
    MRBestWorstMovieByGenre.run()
