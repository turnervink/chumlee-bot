class Level:
    def __init__(self, level: int):
        self.level = level

        if 1 <= self.level < 5:
            self.title = "Chumbaby"
        elif 5 <= self.level < 10:
            self.title = "Chumpeddler"
        else:
            self.title = "I need more level names"
