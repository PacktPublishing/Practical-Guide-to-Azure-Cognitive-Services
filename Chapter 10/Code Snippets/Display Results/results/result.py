class LengthMetaclass(type):
    def __len__(self):
        return self.length()


class Result(metaclass=LengthMetaclass):
    total = 0
    instances = list()

    def __init__(self, file_name, good, bad):
        self.file_name = file_name
        self.good = good
        self.bad = bad
        Result.total += 1
        self.__class__.instances.append(self)

    def passed(self):
        if self.good > self.bad:
            return True
        return False

    def __str__(self):
        return str({
          'file': self.file_name,
          'good': self.good,
          'bad': self.bad,
          'passed': self.passed()
        })

    @classmethod
    def length(cls):
        return Result.total

    @classmethod
    def get_instances(self):
        return Result.instances

    @classmethod
    def unique(self, file_name):
        for result in Result.instances:
            if file_name == result.file_name:
                return False
        return True
