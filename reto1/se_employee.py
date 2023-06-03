from mrjob.job import MRJob

class MRNumSEByEmployee(MRJob):

    def mapper(self, _, line):
        idemp, sector, salary, year = line.split(',')
        yield (idemp, sector), 1

    def reducer(self, keys, values):
        yield keys[0], sum(values)

if __name__ == '__main__':
    MRNumSEByEmployee.run()
