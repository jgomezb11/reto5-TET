from mrjob.job import MRJob
from mrjob.step import MRStep

class MRLeastMoviesDay(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield date, 1

    def reducer(self, date, counts):
        yield date, sum(counts)

    def reducer_find_min_day(self, _, date_count_pairs):
        min_day = min(date_count_pairs, key=lambda x: x[1])
        yield 'Least movies day', min

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_min_day)
        ]

if __name__ == '__main__':
    MRLeastMoviesDay.run()
