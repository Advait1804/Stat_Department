import mysql.connector
import pandas as pd

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Advait@18"
DB_NAME = "Kho_Kho_DB"


EXPECTED_TABLES = [
    "Team",
    "Player",
    "Season",
    "Tournament",
    "Match_details",
    "Match_Stats",
    "Match_Awards",
    "Player_match_stat",
    "Player_season_stat",
    "Player_Role_History",
    "Team_stat",
    "Team_Attack",
    "Team_Defence",
    "Player_Attack",
    "Player_Defence"
]

def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        
    )
def fetch_tables(conn):
    dfs = {}
    for table in EXPECTED_TABLES:
        try:
            dfs[table.lower()] = pd.read_sql(f"SELECT * FROM `{table}`", conn)
        except:
            dfs[table.lower()] = None
    return dfs

