"""
jockey module is the main module for hockeyjockey
"""
import os
import json

import menyou as mn
import colors as col
import hockeyjockey.api as api
import hockeyjockey.models as mod
import hockeyjockey.utilities as ut
from hockeyjockey import config as cfg
import hockeyjockey.exceptions as hj_exceptions


class Jockey(object):
    """
    The main hockeyjockey class. Takes care of instantiating Menus, loading data, and performing calculations.
    """

    def __init__(self, suppress_prompt: bool = True) -> None:
        """
        Initializer. suppress_prompt allows the Menu class' prompt_for_cache user prompt to be surpressed.
        Warning: suppressing this prompt may lead to stale data from disk being loaded.  See the Menu class'
        prompt_for_cached method definition for more information on how to configure this option.

        :param suppress_prompt: A boolean indicating if the prompt_for_cached prompt should be suppressed.
        """
        # TODO: some of these class attributes may no longer be needed.
        # Init menus
        self.menu_main = None
        self.menu_games = None
        self.menu_stats = None
        self.menu_teams = None

        # Stored hockey data
        self.games = []
        self.teams = []

        # Files and paths - defaults can be set in hockeyjockey/config.py
        self.hj_dir = None
        self.teams_file = None
        self.stats_file = None
        self.games_file = None

        # Flags - defaults can be set in hockeyjockey/config.py
        self.suppress_prompt = suppress_prompt
        self.use_cached_games = False
        self.use_cached_stats = False

        # Loaders
        if self.suppress_prompt:
            self.use_cached_games = cfg.suppress.use_games
            self.use_cached_stats = cfg.suppress.use_stats
        else:
            self.use_cached()

        self.load_filepaths()
        self.load_menus()
        self.load_teams()
        self.load_cached_games()

    def use_cached(self):
        """
        Stores the user's preference as to whether or not they wish to use data that has been cached to disk.

        :return: None.
        """
        self.use_cached_stats, self.use_cached_games = Menu.prompt_for_cached()

    def load_filepaths(self):
        """
        Creates the hockeyjockey directory and files for caching data.

        :return: None.
        """
        self.hj_dir = ut.get_hj_dir()
        if self.hj_dir:
            self.teams_file = ut.get_hj_file_path(self.hj_dir, cfg.file.teams_file)
            self.games_file = ut.get_hj_file_path(self.hj_dir, cfg.file.games_file)

    def load_menus(self) -> None:
        """
        Loads the HockeyJockey Menu objects. This represents the main menu structure of HockeyJockey.

        :return: None.
        """

        print('Loading menus... ', end='')

        self.menu_teams = mn.Menyou('Teams', 'Teams menu',
                                    [mn.Opshin(name='Print Teams', payload=self.print_teams)
                                     ],
                                    'Make your selection: ')

        self.menu_stats = mn.Menyou('Stats', 'Stats menu',
                                    [mn.Opshin(name='Reload Stats', payload=self.reload_stats),
                                     mn.Opshin(name='Rank Games by Single Statistic', payload=self.rank_stat_menu_call),
                                     mn.Opshin(name='Rank Games by All Statistics', payload=self.rank_all_menu_call),
                                     mn.Opshin(name='Print Stats', payload=self.print_stats)
                                     ],
                                    'Make your selection: ')

        self.menu_games = mn.Menyou('Games', 'Games menu',
                                    [mn.Opshin(name='Load Today\'s Games', payload=self.load_todays_games),
                                     mn.Opshin(name='Load Yesterday\'s Games', payload=self.load_yesterdays_games),
                                     mn.Opshin(name='Load Upcoming Friday/Saturday Games',
                                               payload=self.load_fri_sat_games),
                                     mn.Opshin(name='Load Games for Custom Date Range', payload=self.load_custom_games_menu_call),
                                     mn.Opshin(name='Print Games', payload=self.print_games)
                                     ],
                                    'Make your selection: ')

        self.menu_main = mn.Menyou('Hockey Jockey', 'Main Menu',
                                   [mn.Opshin(name='Games', payload=self.menu_games),
                                    mn.Opshin(name='Teams', payload=self.menu_teams),
                                    mn.Opshin(name='Stats', payload=self.menu_stats),
                                    mn.Opshin(name='Exit', payload=mn.Menyou.exit)
                                    ],
                                   'Make your selection: ')
        print('Done.')

    # LOADING FUNCTIONS
    def load_teams(self) -> None:
        """
        Loads the teams from disk if they exist, otherwise loads the teams from the internet (statsapi). Teams contain
        the team statistics, so if the user elected to download fresh stats from the internet, load_teams will call
        load_stats to achieve this. Otherwise 'stale' stats will be loaded from disk. The parameter that controls this
        behaviour can be set in hockeyjockey/config.py, or by instantiating Jockey with suppress_prompt=False, in order
        that the user is prompted to make a decision on downloaded vs. cached stats each time the program is run.
        """
        # Disk load
        if os.path.exists(self.teams_file):
            print('Loading teams from disk... ', end='')

            # DESERIALIZE - leave as an empty array if there is an error
            self.teams = ut.deserialize(self.teams_file) or []
            if self.teams:
                print('Done.')
                # The teams file might contain cached stats
                # If this is not desired...
                if not self.use_cached_stats:
                    # ...wipe the stats and load from internet
                    for t in self.teams:
                        t.clear_stats()
                    self.load_stats()
                return

        # Download
        print('Downloading teams... ', end='')
        client = api.NHLApiClient()
        teams = json.loads(client.team_data())

        for team in teams['teams']:
            hj_team = mod.Team(team['id'], team['name'], team['abbreviation'])
            self.teams.append(hj_team)

        if not self.teams:
            raise hj_exceptions.NoTeams('No teams were loaded from statsapi.')

        # Now load the stats
        self.load_stats()

        # SERIALIZE
        ut.serialize(self.teams, self.teams_file)
        print('Done.')

    def load_custom_games(self, start_date: str, end_date: str) -> None:
        """
        Loads games from the internet(statsapi) for a custom date range. During normal execution of Jockey, the Menu
        class provides a function prompt_for_dates that queries the user and validates the dates before passing them to
        this function.

        :param start_date: A string-formatted start date
        :param end_date: A string-formatted end date
        :return: None.
        """
        print(f'Loading games between {start_date} and {end_date}...', end='')
        client = api.NHLApiClient()
        schedule = json.loads(client.schedule_range(start_date, end_date))
        self.json_to_games(schedule)
        print('Done.')

    def load_yesterdays_games(self) -> None:
        """
        Loads the games for yesterday's date from the internet (statsapi).

        :return: None.
        """
        yesterday = ut.yesterday()
        self.load_custom_games(yesterday, yesterday)

    def load_todays_games(self) -> None:
        """
        Loads the games for today's date from the internet (statsapi).

        :return: None.
        """
        today = ut.today()
        # Passing today in manually because the statsapi would sometimes give yesterday's games
        # for the default (supposed to be today's)
        self.load_custom_games(today, today)

    def load_fri_sat_games(self) -> None:
        """
        Loads the games for this Friday and Saturday's games (if the current day is a Friday or Saturday. Otherwise
        loads the games for next Friday and Saturday. This is hockeyjockey's default setting.
        Why? Because the hockey pool I created this application for runs for Friday and Saturday games.

        :returns: None.
        """
        fri, sat = ut.closest_fri_sat()
        self.load_custom_games(fri, sat)

    def load_cached_games(self) -> None:
        """
        Loads the games from disk cache and stores them in the games list attribute. If loading fails, loads the
        closest Friday/Saturday games from the internet (statsapi).

        :return: None.
        """
        # Clear existing games
        self.games.clear()

        # Disk load
        if self.use_cached_games and os.path.exists(self.games_file):
            print('Loading matchups from disk... ', end='')

            # DESERIALIZE - Leave as empty array if there is an error
            self.games = ut.deserialize(self.games_file) or []
            if self.games:
                print('Done.')
                return

        # Download - default to Friday/Saturday games
        self.load_fri_sat_games()

    def json_to_games(self, schedule: 'json string') -> None:
        """
        Clears the current games and loads games from the json string argument (from statsapi). Also populates
        games.data file. If the game has already been played, it populates the winner. Games are stored in the
        games list attribute.

        :param: schedule: A json-formatted string from the statsapi response object.
        :return: None.
        """
        self.games.clear()

        for date in schedule['dates']:
            for game in date['games']:
                gm_date = date['date']
                h_id = game['teams']['home']['team']['id']
                a_id = game['teams']['away']['team']['id']
                h_score = game['teams']['home']['score']
                a_score = game['teams']['away']['score']
                gm_state = game['status']['detailedState']

                gm = None
                if gm_state == 'Final':
                    win_id = h_id if h_score >= a_score else a_id
                    gm = mod.Game(
                        home_team=self.get_team_by_id(h_id),
                        away_team=self.get_team_by_id(a_id),
                        date=gm_date,
                        winning_team=self.get_team_by_id(win_id))
                else:
                    gm = mod.Game(home_team=self.get_team_by_id(h_id),
                                  away_team=self.get_team_by_id(a_id),
                                  date=gm_date)

                self.games.append(gm)

        if not self.games:
            raise hj_exceptions.NoGames('No games were loaded from the statsapi.')

        # SERIALIZE
        ut.serialize(self.games, self.games_file)

    def load_stats(self) -> None:
        """
        Loads team statistics from the internet (statsapi) on a team-by-team basis and stores them in the stats
        attribute of the Team instance they belong to.  Teams must be loaded before this method can be executed. Any
        teams that are missing from the Jockey teams list attribute will not receive their statistics.

        :return: None.
        """
        if not self.teams:
            raise hj_exceptions.NoTeams('No teams have been loaded. Cannot add stats to nonexistent teams.')

        print('Downloading stats... ', end='')
        client = api.NHLApiClient()

        for team in self.teams:
            stats = json.loads(client.single_team_stats(team.id))

            t_stats = None

            for stat_type in stats['stats']:
                if stat_type['type']['displayName'] == 'statsSingleSeason':
                    for split in stat_type['splits']:
                        # Add additional calculated stats here:
                        pdo = ut.calc_pdo(ut.floatize(split['stat']['shootingPctg']),
                                          ut.floatize(split['stat']['savePctg']))
                        t_stats = mod.TStats(pdo=ut.floatize(pdo),
                                             **{k: ut.floatize(v) for k, v in split['stat'].items()})
            team.stats = t_stats
        print('Done.')

    def reload_stats(self):
        """
        Reloads statistical data from the internet and overwrites the current cached data on disk. This also clears any
        current statistical comparisons and rankings.

        :return: None.
        """

        if not self.teams:
            raise hj_exceptions.NoTeams('No teams have been loaded. Cannot add stats to nonexistent teams.')

        print('Reloading stats...', end='')

        # Clear some existing data
        for t in self.teams:
            t.clear_stats()

        # Load the stats
        self.load_stats()

        print('Done.')

    # MENU TRAFFIC DIRECTION
    @staticmethod
    def prompt_for_dates() -> tuple:
        """
        Prompts the user to enter a start date and an end date.  Loops until a valid start date and end date have
        been entered. Dates must match the format supplied in hockeyjockey/config.py in the date namedtuple. At the time
        this docuementation was written, the date format is 'YYYY-MM-DD', which corresponds to the NHL Stats API. See
        https://gitlab.com/dword4/nhlapi for the API documentation.

        :return:  A tuple containing a string-formatted start date and end date.
        """

        def date_prompt(date_type: str) -> str:
            """
            Prompts the user to enter a date as specified by date_type. Loops until a valid date is provided.

            :param date_type: An string displayed in the date entry prompt. i.e. 'start date'.
            :return: A string-formatted date.
            """
            print()
            while True:
                date_str = input(f'Enter {date_type} date <{ut.DATE_STR}>: ')
                return ut.valid_date(date_str) or date_prompt(date_type)

        return date_prompt('start'), date_prompt('end')

    def prompt_for_stat(self, stat_keys: list) -> int:
        """
        Displays a list of statistics available for comparision and prompts the user to choose one. Loops until the
        user enters a valid stat. stat_keys are provided by a Jockey instance (see the Menu class' payload_director
        function to see the mechanism of how this is achieved).
        Displays the stats in a way that wraps the screen when the list of stats is too long. The desired screen width
        can be controlled with the hockeyjockey/config.py ts (TeamStatsPrintConfig) namedtuple, or a global screen
        width can be set at the top of the hockeyjockey/config.py file.

        :param stat_keys: A list of statistic key names provided by a Jockey instance.
        :return: The integer index of the stat.
        """
        print()

        key_wid = max(map(lambda x: len(x), stat_keys))
        idx_wid = 2
        acc_wid = 0
        stats_str = ''

        for i, f in enumerate(stat_keys):

            acc_wid += (idx_wid + 1 + key_wid + 1)
            if acc_wid >= cfg.ts.scr_wid:
                acc_wid = idx_wid + 1 + key_wid + 1
                stats_str += '\n'

            stats_str += f'{i:>{idx_wid + 1}}. {f:<{key_wid + 1}}'

        print(stats_str)
        print()
        choice = None
        while True:
            try:
                choice = int(input('Enter the number of the stat you wish to compare: '))
            except ValueError:
                self.choice_invalid()
            if choice in range(len(stat_keys)):
                return choice
            else:
                self.choice_invalid()

    def load_custom_games_menu_call(self) -> None:
        """
        This function is called by Menu and execute the functions required to load custom games.

        :return: None.
        """
        start_date, end_date = self.prompt_for_dates()
        self.load_custom_games(start_date, end_date)

    def rank_stat_menu_call(self) -> tuple:
        """
        This function is called by Menu and executes the functions required to print the user-selected stat.

        :return: None.
        """
        s_keys = self.get_stat_keys()
        s_idx = self.prompt_for_stat(s_keys)
        self.compare_all()
        self.rank_all()
        self.print_stat_ranked(stat_idx=s_idx)

    def rank_all_menu_call(self) -> None:
        """
        This function is called by Menu and executes the functions required to print all the stats.

        :return: None.
        """
        self.compare_all()
        self.rank_all()
        self.print_all_ranked()

    # CALCULATING/RANKING FUNCTIONS
    def compare_all(self) -> None:
        # TODO - once things are compared, we should re-use the comparisons unless new games are loaded. Same for
        # rankings.
        """
        Compares statistics of each stored statistic type between every Game object stored in the games list
        attribute (i.e. Montreal has 10 wins and Toronto has 20 wins. The comparison for the stat 'wins' is +10 because
        Toronto is the home team: diff = home_stat - away_stat).
        The results of these comparisons are stored on a game-by-game basis in the games attribute under the Game
        class' comparisons attribute.  comparisons is a dictionary with the stat name as the key and the comparison
        difference as the value.

        :return: None.
        """
        if not self.teams:
            raise hj_exceptions.NoTeams('No teams have been loaded. Cannot compare stats without teams.')
        if not self.games:
            raise hj_exceptions.NoGames('No games have been loaded. Cannot compare stats without games.')

        s_keys = self.get_stat_keys()
        for idx, gm in enumerate(self.games):
            for s_key in s_keys:
                a_stat = getattr(gm.a.stats, s_key)
                h_stat = getattr(gm.h.stats, s_key)
                diff = h_stat - a_stat
                gm.comparisons[s_key] = diff

    def rank_all(self) -> None:
        """
        Ranks all of the comparisons generated by the compare_all method. Comparisons are ranked for the games in
        memory, for each stat key, from least(Rank=1) to Most(Rank=Number of Games) by the match up's absolute
        difference between compared statistics.

        :return: None.
        """
        if not self.teams:
            raise hj_exceptions.NoTeams('No teams have been loaded. Cannot rank games without teams.')
        if not self.games:
            raise hj_exceptions.NoGames('No games have been loaded. Cannot rank games without games.')

        s_keys = self.get_stat_keys()
        for s_key in s_keys:
            games = sorted(self.games, key=lambda x: abs(x.comparisons[s_key]))
            for rank, game in enumerate(games, start=1):
                game.ranks[s_key] = rank

    # PRINTING FUNCTIONS
    def print_teams(self) -> None:
        """
        Prints a list of the teams that are loaded. Nothing fancy - this should just be a list of the names and
        abbreviations of each NHL hockey team with the statsapi team_id.  The team_id could be useful if one wanted to
        query the statsapi directly.
        Print formatting (column widths) can be controlled via hockeyjockey/config.py by the tm (TeamPrintConfig)
        namedtuple.

        :return: None.
        """
        print()
        print(
            f'{"Team ID":>{cfg.tm.id_wid}} |{"Abbreviation":>{cfg.tm.abbrev_wid}} |{"Team Name":>{cfg.tm.name_wid}}')
        print('-' * (cfg.tm.id_wid + cfg.tm.abbrev_wid + cfg.tm.name_wid + 4))
        print(*sorted(self.teams, key=lambda x: x.name), sep='')
        print()

    def print_games(self) -> None:
        """
        Prints a list of the games that are currently loaded. If the games occurred in the past, will also display the
        winner. Print formatting (column widths) can be controlled via hockeyjockey/config.py gm (GamePrintConfig)
        named tuple.
        :return:
        """
        print()
        print(f'{"Date":>{cfg.gm.dt_wid}} |'
              f'{"Away":>{cfg.gm.team_wid}} |'
              f'{"Home":>{cfg.gm.team_wid}} |'
              f'{"Winner":>{cfg.gm.team_wid}}')
        print('-' * (cfg.gm.dt_wid + cfg.gm.team_wid * 3 + 6))
        print(*self.games, sep='')
        print()

    def print_stats(self) -> None:
        """
        Prints a list of the currently loaded NHL statistics, separated by a header for each team. Print formatting
        (screen width and column width) can be controlled via the hockeyjockey/config.py ts (TeamStatsPrintConfig)
        namedtuple.

        :return: None.
        """

        if not self.teams:
            print('No teams have been loaded. Cannot print stats.')
        else:
            print()
            for t in sorted(self.teams, key=lambda x: x.name):
                cur_stats = t.stats
                title_str = f'Stats for team: {t.name:<{cfg.ts.key_wid}}'
                print(f'{title_str:^{cfg.ts.scr_wid}}')
                print(f'-' * cfg.ts.scr_wid)
                print(cur_stats)
                print()
            print()

    def print_stat_ranked(self, stat_idx: int) -> None:
        """
        Prints the rankings for a single stat, for all of the games in memory. The team who would theoretically win
        is highlighted in green.
        """
        desired_r_wid = cfg.r.rank_wid
        desired_h_wid = desired_a_wid = cfg.r.team_wid

        print()
        print(
            f'{"Away":^{cfg.r.team_wid}}|'
            f'{"Home":^{cfg.r.team_wid}}|'
            f'{"Diff":>{cfg.r.diff_wid}} | '
            f'{"Rank":>{cfg.r.rank_wid}}')

        print('-' * (cfg.r.team_wid * 2 + 5 + cfg.r.diff_wid + cfg.r.rank_wid))

        for idx, gm in enumerate(self.games):

            a_abbrev = gm.a.abbrev
            h_abbrev = gm.h.abbrev
            s_keys = self.get_stat_keys()
            s_key = s_keys[stat_idx]
            diff = gm.comparisons[s_key]

            rank = col.color(str(gm.ranks[s_key]), fg='green')
            rank_wid = desired_r_wid - col.ansilen(rank) + len(rank)

            h_wid = None
            a_wid = None

            if diff >= 0:
                h_abbrev = col.color(h_abbrev, fg='green')
                # Padding
                h_wid = desired_h_wid - col.ansilen(h_abbrev) + len(h_abbrev)

            else:
                a_abbrev = col.color(a_abbrev, fg='green')
                # Padding
                a_wid = desired_a_wid - col.ansilen(a_abbrev) + len(a_abbrev)

            print(
                f'{a_abbrev:^{a_wid or desired_a_wid}}|'
                f'{h_abbrev:^{h_wid or desired_h_wid}}|'
                f'{abs(diff):>{cfg.r.diff_wid}.2f} | '
                f'{rank:>{rank_wid or desired_r_wid}}')

        print()

    def print_all_ranked(self) -> None:
        """
        Prints the rankings for all stats, for all of the games in memory.  The ranks are highlighted green if the
        home team would theoretically win and red if the away team would theoretically win.

        :return: None.
        """
        desired_r_wid = cfg.r.rank_wid
        desired_h_wid = desired_a_wid = cfg.r.team_wid
        stat_keys = self.get_stat_keys()

        print()
        print(
            f'{"Away":^{desired_a_wid}}|'
            f'{"Home":^{desired_h_wid}}|', end='')

        print('|'.join(f'{i:>{desired_r_wid}} ' for i, _ in enumerate(stat_keys)))
        # The +literals in the statement below account for the pipe (|) chars
        print('-' * (desired_h_wid + desired_a_wid + 2 + desired_r_wid * len(stat_keys) + 2 * len(stat_keys)))

        for gm in self.games:

            a_abbrev = gm.a.abbrev
            h_abbrev = gm.h.abbrev

            print(
                f'{a_abbrev:^{desired_a_wid}}|'
                f'{h_abbrev:^{desired_h_wid}}|', end='')

            for s_idx, s_key in enumerate(stat_keys):
                diff = gm.comparisons[s_key]

                rank = gm.ranks[s_key]
                r_wid = None

                if diff >= 0:
                    rank = col.color(rank, fg='green')
                    # Padding
                    r_wid = desired_r_wid - col.ansilen(rank) + len(rank)

                else:
                    rank = col.color(rank, fg='red')
                    # Padding
                    r_wid = desired_r_wid - col.ansilen(rank) + len(rank)

                if s_idx < len(stat_keys) - 1:
                    print(f'{rank:>{r_wid or desired_r_wid}} |', end='')
                else:
                    print(f'{rank:>{r_wid or desired_r_wid}}')

        print()

    # HELPFUL FUNCTIONS
    def get_team_by_id(self, id: int) -> 'Team':
        """
        Returns a Team object associated with the id parameter, provided the teams list attribute has been populated
        and id is a valid team id.

        :param id: The integer team id
        :return: a hockeyjockey Team object
        """
        return next(iter(tm for tm in self.teams if tm.id == id))

    def get_stat_keys(self) -> list:
        # TODO - error handling because this might fail
        """
        Returns a list of the statistic key names, provided at least one game has been loaded with team stats from the
        statsapi.

        :return: A list of statistic key names.
        """
        return self.games[0].h.stats.stat_keys

    def get_all_team_stats(self) -> dict:
        """
        Returns a dicionary with team_id as the key that holds the stats for all teams.

        :return: stats dictionary
        """
        s_dict = {}
        for tm in self.teams:
            s_dict[tm.id] = tm.stats

        return s_dict
