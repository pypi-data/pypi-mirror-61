import mysql.connector
import hockeyjockey.config as cfg


def connect(host, user, database, passwd, port=3306):
    try:
        db = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            passwd=passwd
        )
        return db
    except mysql.connector.Error as e:
        print(f'Error connecting to database: {e}')


def hj_connect():
    db = connect(
        host=cfg.db.db_host,
        user=cfg.db.user_rw,
        database=cfg.db.db_name,
        passwd=cfg.db.pass_rw
    )
    return db
