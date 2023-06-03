from mrjob.job import MRJob
from mrjob.step import MRStep

class MRNumSEByEmployee(MRJob):

    def mapper(self, _, line):
        idemp, sector, _, _ = line.split(',')
        yield (idemp, sector), None

    def reducer(self, keys, values):
        yield keys[0], keys[1]

    def reducer_count_sectors(self, idemp, sectors):
        unique_sectors = len(set(sectors))
        yield idemp, unique_sectors

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_count_sectors)
        ]

if __name__ == '__main__':
    MRNumSEByEmployee.run()

