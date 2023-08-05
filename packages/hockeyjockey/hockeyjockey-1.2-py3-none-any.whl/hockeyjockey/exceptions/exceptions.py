class HJException(Exception):
    """Basic exception for errors raised by hockeyjockey"""

    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.errors = errors


class NoGames(HJException):
    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.errors = errors

class NoTeams(HJException):
    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.errors = errors

