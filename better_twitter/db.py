import sqlite3
import pandas as pd
from os import path
from configs import CONFIG_DIR, DB_FILE


def update_db(data, table_name, columns=[]):
    db_path = path.expanduser(path.join(CONFIG_DIR, DB_FILE))
    con = sqlite3.connect(db_path)

    try:
        df = pd.read_sql(f"select * from {table_name}", con=con)
    except:
        df = pd.DataFrame(columns=columns)

    df = df.append(data, ignore_index=True)
    df.to_sql(table_name, con=con, index=False, if_exists="replace")
    return df.shape[0]