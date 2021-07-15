import argparse
import configparser
from os import path, mkdir
import sqlite3
import twitter
import pandas as pd
from tweets import block_from_file
from configs import CONFIG_DIR, CRED_WARNING_MSG, CONFIG_FILE, DB_FILE


def cursive_command():
    api = load_api()
    args = parse()
    if args.block_file:
        block_from_file(api, args.block_file)


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


if __name__ == '__main__':
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
