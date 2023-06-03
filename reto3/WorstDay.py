from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWorstRatingDay(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield date, float(rating)

    def reducer(self, date, ratings):
        ratings_list = list(ratings)
        if ratings_list:
            yield None, (date, sum(ratings_list) / len(ratings_list))
        else:
            yield None, (date, 0)

    def reducer_find_worst_day(self, _, date_avg_rating_pairs):
        worst_day = min(date_avg_rating_pairs, key=lambda x: x[1])
        yield 'Worst rating day', worst_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_worst_day)
        ]

if __name__ == '__main__':
    MRWorstRatingDay.run()
