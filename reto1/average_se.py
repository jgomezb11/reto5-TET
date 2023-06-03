from mrjob.job import MRJob

class MRAvgSalaryBySE(MRJob):

    def mapper(self, _, line):
        idemp, sector, salary, year = line.split(',')
        yield sector, float(salary)

    def reducer(self, sector, salaries):
        total = 0
        num = 0
        for salary in salaries:
            total += salary
            num += 1
        yield sector, total / num

if __name__ == '__main__':
    MRAvgSalaryBySE.run()
