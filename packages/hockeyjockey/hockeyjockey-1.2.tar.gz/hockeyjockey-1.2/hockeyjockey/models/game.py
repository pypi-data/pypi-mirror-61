"""
Game class.
"""
import hockeyjockey.config as cfg
from hockeyjockey.models import Team


class Game(object):
    """
    A hockey game (or matchup) between two teams.
    """

    def __init__(self, home_team: 'Team', away_team: 'Team', date: str, winning_team: 'Team' = -1, ranks: dict = None,
                 comparisons: dict = None) -> None:
        """
        Information about a hockey game. Home Team ID, Away Team ID, date, and Winning Team ID.
        """
        self.h = home_team
        self.a = away_team
        self.date = date
        self.w = winning_team
        self.ranks = ranks or {}
        self.comparisons = comparisons or {}

    def __str__(self):
        """
        Print a game.
        """
        return f'{self.date:>{cfg.gm.dt_wid}} |' \
               f'{self.a.abbrev:>{cfg.gm.team_wid}} |' \
               f'{self.h.abbrev:>{cfg.gm.team_wid}} |' \
               f'{self.w.abbrev if isinstance(self.w, Team) else "N/A":>{cfg.gm.team_wid}}\n'
