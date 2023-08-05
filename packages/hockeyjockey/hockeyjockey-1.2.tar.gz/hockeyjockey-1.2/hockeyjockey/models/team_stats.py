from hockeyjockey import config as cfg


class TStats(object):
    """
    Team statistics.
    """

    def __init__(self, **kwargs):
        """
        Initializer. Imports all keyword arguments passed to it. Stores the keys in stats.keys for easy access later.
        """
        self.__dict__.update(kwargs)

        # Useful so I don't have to deal with the __dict__ for my stat keys
        self.stat_keys = []
        for k, _ in kwargs.items():
            self.stat_keys.append(k)
        self.stat_keys = sorted(self.stat_keys)

    def __str__(self):
        max_key = max(map(lambda x: len(x), self.stat_keys))
        acc_width = 0
        stat_str = ''

        for s_key in sorted(self.stat_keys):
            acc_width += (max_key + 1 + cfg.ts.val_wid + 1)
            if acc_width >= cfg.ts.scr_wid:
                acc_width = max_key + 1 + cfg.ts.val_wid + 1
                stat_str += '\n'

            stat_str += f'{s_key:>{max_key + 1}}:{getattr(self, s_key):>{cfg.ts.val_wid + 1}.2f}'

        return stat_str
