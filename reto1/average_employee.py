from mrjob.job import MRJob

class MRAvgSalaryByEmployee(MRJob):

    def mapper(self, _, line):
        idemp, sector, salary, year = line.split(',')
        yield idemp, float(salary)

    def reducer(self, idemp, salaries):
        total = 0
        num = 0
        for salary in salaries:
            total += salary
            num += 1
        yield idemp, total / num

if __name__ == '__main__':
    MRAvgSalaryByEmployee.run()
