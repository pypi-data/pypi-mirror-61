from hockeyjockey import config as cfg

class Team(object):
    """
    A hockey team.
    """
    def __init__(self, id, name, abbrev, stats=None):
        """
        Initializer.
        """
        self.id = id
        self.name = name
        self.abbrev = abbrev
        self.stats = stats

    def __str__(self):
        return f'{self.id:>{cfg.tm.id_wid}} |' \
               f'{self.abbrev:>{cfg.tm.abbrev_wid}} |' \
               f'{self.name:>{cfg.tm.name_wid}}\n'

    def clear_stats(self):
        self.stats = None

