import argparse
import configparser
from os import path, mkdir
import sqlite3
import twitter
import pandas as pd
import pendulum as pn
import time


CRED_WARNING_MSG = "You first need to enter the credentials received from Twitter."
CONFIG_DIR = "~/.better-twitter"
CONFIG_FILE = "config.ini"
DB_FILE = "data.db"


def cursive_command():
    api = load_api()

    db_path = path.expanduser(path.join(CONFIG_DIR, DB_FILE))
    con = sqlite3.connect(db_path)

    try:
        df_accounts = pd.read_sql("select * from accounts", con=con)
    except:
        df_accounts = pd.DataFrame(columns=["user_id", "screen_name"])
    df_accounts["user_id"] = df_accounts["user_id"].astype(int)

    args = parse()
    if args.block_file:
        block_from_file(api=api, file_path=args.block_file, df_accounts=df_accounts)
    elif args.update_api:
        update_api()


def load_api():
    config = configparser.ConfigParser()
    config_path = path.expanduser(path.join(CONFIG_DIR, CONFIG_FILE))
    if path.exists(config_path):
        config.read(config_path)
    else:
        print(CRED_WARNING_MSG)
        config["DEFAULT"]["consumer_key"] = input("Consumer Key: ")
        config["DEFAULT"]["consumer_secret"] = input("Consumer Secret: ")
        config["DEFAULT"]["access_token_key"] = input("Access Token Key: ")
        config["DEFAULT"]["access_token_secret"] = input("Access Token Secret: ")

        if not path.exists(path.expanduser(CONFIG_DIR)):
            mkdir(path.expanduser(CONFIG_DIR))

        with open(config_path, "w") as config_file:
            config.write(config_file)
            
    try:
        api = twitter.Api(
            consumer_key=config["DEFAULT"]["consumer_key"],
            consumer_secret=config["DEFAULT"]["consumer_secret"],
            access_token_key=config["DEFAULT"]["access_token_key"],
            access_token_secret=config["DEFAULT"]["access_token_secret"]
        )
    except KeyError:
        print(CRED_WARNING_MSG)
        update_api()
        api = load_api()
    return api


def update_api():
    config = configparser.ConfigParser()
    config_path = path.expanduser(path.join(CONFIG_DIR, CONFIG_FILE))
    config.read(config_path)
    new_consumer_key = input("Consumer Key (leave blank if you don't want to update it): ")
    if new_consumer_key:
        config["DEFAULT"]["consumer_key"] = new_consumer_key
    new_consumer_secret = input("Consumer Secret (leave blank if you don't want to update it): ")
    if new_consumer_secret:
        config["DEFAULT"]["consumer_secret"] = new_consumer_secret
    new_access_token_key = input("Access Token Key (leave blank if you don't want to update it): ")
    if new_access_token_key:
        config["DEFAULT"]["access_token_key"] = new_access_token_key
    new_access_token_secret = input("Access Token Secret (leave blank if you don't want to update it): ")
    if new_access_token_secret:
        config["DEFAULT"]["access_token_secret"] = new_access_token_secret

    with open(config_path, "w") as config_file:
        config.write(config_file)
    print("The twitter api credentials have been updated successfully.")
    return None


def parse():
    parser = argparse.ArgumentParser(
        description="Make twitter a better place with multiple options.")

    parser.add_argument(
        "--block-file", 
        action="store", 
        type=str, 
        required=False,
        help="Block multiple users from a file at once."
    )
    parser.add_argument(
        "--update-api", 
        action="store_true", 
        required=False,
        help="Update twitter api credentials."
    )
    return parser.parse_args()


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


def block_from_file(api, file_path, df_accounts):
    df = pd.read_csv(file_path)
    if "user_id" not in df.columns or "screen_name" not in df.columns:
        raise Exception("The file should have both user_id and screen_name columns.")
    df["user_id"] = df["user_id"].astype(int)
    print(f"Blocking {df.shape[0]} users from file ...")
    for i, row in df.iterrows():
        if row["user_id"] in df_accounts["user_id"].values:
            print(f"User is already blocked: {row['screen_name']}")
            continue
        try:
            response = api.CreateBlock(user_id=row.user_id)
        except twitter.error.TwitterError as e:
            if e.message[0]["code"] == 50:  # User not found
                print(f"User not found: {row['screen_name']}")
                data = {
                    "user_id": row["user_id"],
                    "last_checked": str(pn.now()),
                    "comment": "User not found",
                }
                update_db(data, "accounts")
            elif e.message[0]["code"] == 88:  # rate limit
                print("API rate limit. Waiting for 5 minutes ...")
                time.sleep(300)
                pass
            elif e.message[0]["code"] == 89:  # Invalid or expired token
                print(e.message[0]["message"])
                print("You need to add valid tokens with following command first:\nbetter-twitter --update-api")
                return None
            else:
                raise Exception(e.message)
        else:
            data = {
                "user_id": row["user_id"],
                "screen_name": response.screen_name,
                "followers_count": response.followers_count,
                "followings_count": response.friends_count,
                "account_created_at": response.created_at,
                "last_checked": str(pn.now()),
            }
            update_db(data, "accounts")
            print(f"Blocked user: {row.screen_name}")
    return None


if __name__ == '__main__':
    cursive_command()