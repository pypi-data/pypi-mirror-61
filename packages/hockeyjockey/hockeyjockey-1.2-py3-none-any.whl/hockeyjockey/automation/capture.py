import mysql
from hockeyjockey import Jockey
from hockeyjockey import models as mod
from hockeyjockey.utilities.db import hj_connect
from mysql.connector import errorcode
from hockeyjockey import models as mod
import hockeyjockey.config as cfg
from time import sleep
import sys
from hockeyjockey import exceptions as hj_exceptions

def capture_winners() -> None:
    """
    This function is meant to run on a nightly basis via an automated process (such as a CRON job). It will look up
    the winners of the previous night's games and populate the games table in the hockey_jockey database.

    :return: None.
    """
    atts = 0
    att_target = cfg.db_cap.attempts
    j_timeout = cfg.db_cap.jockey_timeout
    j = None
    success = False

    while atts <= att_target:
        try:
            j = Jockey(suppress_prompt=True)
            j.load_yesterdays_games()

        except hj_exceptions.NoGames as e:
            print(e)
        else:
            # No exceptions encountered
            print('hockeyjockey has been loaded. Continuing.')
            success = True
        finally:
            if not success:
                if atts == att_target:
                    print('Maximum attempts have been reached. Aborting.')
                    sys.exit(0)
                else:
                    print(f'Will try again in {j_timeout} seconds.')
                    j = None
                    sleep(j_timeout)
                    atts += 1
            else:
                # Success
                break

    cnx = hj_connect()
    cursor = cnx.cursor()

    for gm in j.games:
        h_id = gm.h.id
        a_id = gm.a.id
        # If we stored a team, there is a winner. -1 indicates the game has not yet been played.
        w_id = gm.w.id if isinstance(gm.w, mod.Team) else gm.w
        dt = gm.date

        if w_id == -1:
            print(f'The game between {gm.a.abbrev} and {gm.h.abbrev} for {dt} has not been played yet. Cannot fill the winner.')
            continue

        # get the id of the game to update
        gm_query = ("(SELECT id FROM games WHERE a_id = %s AND h_id = %s AND gm_dt = DATE_FORMAT(%s, '%Y-%m-%d %T'))")

        cursor.execute(gm_query, (a_id, h_id, dt))
        gm_id, *_ = cursor.fetchone()

        if not gm_id:
            print(f'No game found in database matching away_id: {a_id}, home_id: {h_id}, and date: {dt}')
        else:
            print(f'Found a game in the database matching away_id: {a_id}, home_id: {h_id}, and date: {dt}')
            print(f'The winner was {gm.w.abbrev}')
            print(f'Updating the daily_ranks table.')
            add_winner = ("UPDATE daily_ranks SET actual_winner_id = %s WHERE game_id = %s")
            cursor.execute(add_winner, (w_id, gm_id))
    cnx.commit()
    cursor.close()
    cnx.close()

def capture_predictions() -> None:
    """
    This function is meant to run on a daily basis via an automated process (such as a CRON job). It will calculate the
    rankings for the games to be played today in all stat categories and store them in the hockey_jockey database.

    :return: None.
    """
    # If jockey encounters exceptions or doesn't load any games, keep trying every n minutes.
    atts = 0
    att_target = cfg.db_cap.attempts
    j_timeout = cfg.db_cap.jockey_timeout
    j = None
    success = False

    while atts <= att_target:
        try:
            j = Jockey(suppress_prompt=True)
            j.load_todays_games()
            j.compare_all()
            j.rank_all()
        except hj_exceptions.NoGames as e:
            print(e)
        else:
            # No exceptions encountered
            print('hockeyjockey has been loaded. Continuing.')
            success = True
        finally:
            if not success:
                if atts == att_target:
                    print('Maximum attempts have been reached. Aborting.')
                    sys.exit(0)
                else:
                    print(f'Will try again in {j_timeout} seconds.')
                    j = None
                    sleep(j_timeout)
                    atts += 1
            else:
                # Success
                break

    # Teams shouldn't change, but we check anyway
    capture_teams(j.teams)

    # Stat definitions shouldn't change, but we check anyway
    capture_stat_defs(j.get_stat_keys())

    # Load the team stats
    capture_stats(j.get_all_team_stats())

    # Capture games if we haven't already today
    capture_games(j.games)

    # Capture rankings if we haven't already today
    capture_ranks(j.games)


def capture_teams(teams: list) -> None:
    # Connect to hockey_jockey db
    cnx = hj_connect()
    cursor = cnx.cursor()
    tm_query = ("SELECT COUNT(*) FROM teams_def")
    cursor.execute(tm_query)
    tm_cnt, *_ = cursor.fetchone()

    if len(teams) == tm_cnt:
        print('Team count in Jockey matches team count in database. No action taken.')
    elif len(teams) > tm_cnt:
        print('Some teams are missing. Adding them now...')
        for tm in teams:
            try:
                add_team = ("INSERT INTO teams_def (id, abbrev, name) VALUES (%s, %s, %s)")
                cursor.execute(add_team, (tm.id, tm.abbrev, tm.name))
            except mysql.connector.IntegrityError as e:
                print(e)
                continue

        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        print('There are more teams in the database than the statsapi returned. Something is wrong.')


def capture_stat_defs(s_keys: list) -> None:
    # Connect to hockey_jockey db
    cnx = hj_connect()
    cursor = cnx.cursor()
    s_query = ("SELECT COUNT(*) FROM stat_def")
    cursor.execute(s_query)
    s_cnt, *_ = cursor.fetchone()

    if len(s_keys) == s_cnt:
        print('Stats count in Jockey matches team count in database. No action taken.')
    elif len(s_keys) > s_cnt:
        print('Some stats are missing. Adding them now...')
        for s_key in s_keys:
            try:
                add_team = ("INSERT INTO stat_def (statsapi_name, readable_name) VALUES (%s, %s)")
                cursor.execute(add_team, (s_key, s_key))
            except mysql.connector.IntegrityError as e:
                print(e)
                continue

        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        print('There are more stats in the database than the statsapi returned. Something is wrong.')


def capture_games(games: list) -> None:
    # Connect to hockey_jockey db
    cnx = hj_connect()
    cursor = cnx.cursor()

    gm_query = ("SELECT COUNT(*) FROM games WHERE DATE(created_at) = CURDATE()")
    add_games = ("INSERT INTO games (a_id, h_id, gm_dt) VALUES (%s, %s, %s)")

    cursor.execute(gm_query)
    gm_cnt, *_ = cursor.fetchone()

    if gm_cnt > 0:
        print('Games have already been loaded for today. Skipping game load.')
        return None
    else:
        print('Loading new games')
        for gm in games:
            try:
                cursor.execute(add_games, (gm.a.id, gm.h.id, gm.date))
            except mysql.connector.IntegrityError as e:
                print(e)
                continue

    cnx.commit()
    cursor.close()
    cnx.close()


def capture_stats(stats: dict) -> None:
    # Connect to hockey_jockey db
    cnx = hj_connect()
    cursor = cnx.cursor()

    s_query = ("SELECT COUNT(*) FROM daily_stats WHERE DATE(created_at) = CURDATE()")
    add_stats = ("INSERT INTO daily_stats (team_id, stat_def_id, value) VALUES (%s, (SELECT id FROM stat_def WHERE "
                 "statsapi_name = %s), %s)")

    cursor.execute(s_query)
    s_cnt, *_ = cursor.fetchone()

    if s_cnt > 0:
        print('Stats have already been loaded for today. Skipping stat load.')
        return None
    else:
        print('Loading new stats')
        for tm in stats:
            tm_id = tm
            tm_stats = stats[tm]
            for s_key in tm_stats.stat_keys:
                cursor.execute(add_stats, (tm_id, s_key, getattr(tm_stats, s_key)))

    cnx.commit()
    cursor.close()
    cnx.close()


def capture_ranks(games: list) -> None:
    # Connect to hockey_jockey db
    cnx = hj_connect()
    cursor = cnx.cursor()

    r_query = ("SELECT COUNT(*) FROM daily_ranks WHERE DATE(created_at) = CURDATE()")
    # TODO - this query incomplete
    add_ranks = (
        "INSERT INTO daily_ranks (ranking, game_id, stat_def_id, pred_winner_id, actual_winner_id) VALUES (%s, (SELECT id FROM "
        "games WHERE a_id = %s AND h_id = %s AND gm_dt = DATE_FORMAT(%s, '%Y-%m-%d %T')), (SELECT id FROM stat_def WHERE statsapi_name ="
        " %s), %s, %s)")

    cursor.execute(r_query)
    r_cnt, *_ = cursor.fetchone()

    if r_cnt > 0:
        print('Ranks have already been loaded for today. Skipping rank load.')
        return None
    else:
        print('Loading new rankings')
        # iterate through games
        for gm in games:
            for s_key in gm.ranks:
                pred_win_id = gm.h.id if gm.comparisons[s_key] >= 0 else gm.a.id
                cursor.execute(add_ranks, (gm.ranks[s_key], gm.a.id, gm.h.id, gm.date, s_key, pred_win_id, pred_win_id))
    cnx.commit()
    cursor.close()
    cnx.close()
