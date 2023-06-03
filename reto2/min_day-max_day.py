from mrjob.job import MRJob

class MRMinMaxPriceByCompany(MRJob):

    def mapper(self, _, line):
        company, price, date = line.split(',')
        yield company, (float(price), date)

    def reducer(self, company, price_date_pairs):
        min_price_date = max_price_date = next(price_date_pairs)
        for price_date in price_date_pairs:
            if price_date[0] < min_price_date[0]:
                min_price_date = price_date
            elif price_date[0] > max_price_date[0]:
                max_price_date = price_date
        yield company, (min_price_date, max_price_date)

if __name__ == '__main__':
    MRMinMaxPriceByCompany.run()
