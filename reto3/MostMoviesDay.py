from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMostMoviesDay(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield date, 1

    def reducer(self, date, counts):
        yield date, sum(counts)

    def reducer_find_max_day(self, _, date_count_pairs):
        max_day = max(date_count_pairs, key=lambda x: x[1])
        yield 'Most movies day', max_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_max_day)
        ]

if __name__ == '__main__':
    MRMostMoviesDay.run()
