class DataOB:
    def __init__(self, city_name, author, sort, num_range, time):
        self.city_name = city_name
        self.author = author
        self.sort = sort
        self.num_range = num_range
        self.time = time

    def __repr__(self):
        return "省/城市名: " + self.city_name + " |车管所: " + self.author + " |汽车种类: " + self.sort + " |牌照号段: " + self.num_range + " |时间: " + self.time


class TerminationStatusRecord:
    def __init__(self, url, author_num, sort_num):
        self.url = url
        self.author_num = author_num
        self.sort_num = sort_num

