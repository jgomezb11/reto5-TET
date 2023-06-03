from mrjob.job import MRJob
from mrjob.step import MRStep

class MRBestRatingDay(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield date, float(rating)

    def reducer(self, date, ratings):
        ratings_list = list(ratings)
        if len(ratings_list) != 0:
            yield None, (date, sum(ratings_list) / len(ratings_list))

    def reducer_find_best_day(self, _, date_avg_rating_pairs):
        best_day = max(date_avg_rating_pairs, key=lambda x: x[1])
        yield 'Best rating day', best_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_best_day)
        ]

if __name__ == '__main__':
    MRBestRatingDay.run()
