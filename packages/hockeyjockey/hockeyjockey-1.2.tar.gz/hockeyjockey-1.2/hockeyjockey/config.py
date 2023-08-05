"""
Configurations.
"""
from collections import namedtuple
import os

# Global screen width
glbl_scr_width = 120

# Print formatting configuration
TeamStatsPrintConfig = namedtuple('TeamStatsPrintConfig', ('scr_wid', 'key_wid', 'val_wid'))
ts = TeamStatsPrintConfig(scr_wid=glbl_scr_width, key_wid=22, val_wid=7)

GamePrintConfig = namedtuple('GamePrintConfig', ('scr_width', 'dt_wid', 'team_wid'))
gm = GamePrintConfig(scr_width=glbl_scr_width, dt_wid=11, team_wid=8)

TeamPrintConfig = namedtuple('TeamConfig', ('scr_width', 'id_wid', 'name_wid', 'abbrev_wid'))
tm = TeamPrintConfig(scr_width=glbl_scr_width, id_wid=8, name_wid=22, abbrev_wid=13)

RanksPrintConfig = namedtuple('RanksPrintConfig', ('scr_width', 'rank_wid', 'team_wid', 'diff_wid'))
r = RanksPrintConfig(scr_width=glbl_scr_width, rank_wid=5, team_wid=6, diff_wid=9)

# Date formatting
DateConfig = namedtuple('DateConfig', ('date_fmt', 'date_str'))
date = DateConfig(date_fmt='%Y-%m-%d', date_str='YYYY-MM-DD')

# Files and directories for cached data
FileConfig = namedtuple('FileConfig', ('data_dir_loc', 'data_dir_name', 'teams_file', 'games_file'))
file = FileConfig(data_dir_loc='~',
                  data_dir_name='hj_data',
                  teams_file='teams.data',
                  games_file='games.data')

# Config for suppress the prompt to use cached stats when the program loads
MenuSuppressConfig = namedtuple('MenuSuppressConfig', ('use_games', 'use_stats'))
suppress = MenuSuppressConfig(use_games=False, use_stats=False)

# Database
DBConfig = namedtuple('DBConfig', ('user_read', 'pass_read', 'user_rw', 'pass_rw', 'db_host', 'db_name',
                                   'db_port'))
db = DBConfig(db_host=os.environ['DB_HJ_HOST'],
              db_port=os.environ['DB_HJ_PORT'],
              db_name=os.environ['DB_HJ_DATABASE'],
              user_read=os.environ['DB_HJ_USER_READ'],
              pass_read=os.environ['DB_HJ_PASS_READ'],
              user_rw=os.environ['DB_HJ_USER_RW'],
              pass_rw=os.environ['DB_HJ_PASS_RW'])

# Database capture (timeouts, etc)
DBCaptureConfig = namedtuple('DBCaptureConfig', ('attempts', 'jockey_timeout'))
db_cap = DBCaptureConfig(attempts=5, jockey_timeout=600)

