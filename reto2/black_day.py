from mrjob.job import MRJob
from mrjob.step import MRStep

class MRBlackDay(MRJob):

    def mapper(self, _, line):
        company, price, date = line.split(',')
        yield date, float(price)

    def reducer(self, date, prices):
        min_price = min(prices)
        yield None, (date, min_price)

    def reducer_find_black_day(self, _, date_minprice_pairs):
        black_day = min(date_minprice_pairs, key=lambda x: x[1])
        yield 'Black Day', black_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_black_day)
        ]

if __name__ == '__main__':
    MRBlackDay.run()
