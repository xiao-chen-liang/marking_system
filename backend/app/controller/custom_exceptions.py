class TheReportIsNotNewestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotAllCoursesPassedError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

