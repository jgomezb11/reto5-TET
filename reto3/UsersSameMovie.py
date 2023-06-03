from mrjob.job import MRJob

class MRMovieUsers(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.split(',')
        yield movie, (user, float(rating))

    def reducer(self, movie, user_rating_pairs):
        num_users = 0
        total_rating = 0
        for user, rating in user_rating_pairs:
            num_users += 1
            total_rating += rating
        yield movie, (num_users, total_rating / num_users)

if __name__ == '__main__':
    MRMovieUsers.run()
