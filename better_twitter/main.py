from better_twitter import block_from_file
import argparse
import configparser
from os import path
import twitter


def cursive_command():
    api = load_api()
    args = parse()
    if args.block_file:
        block_from_file(api, args.block_file)


def load_api():
    config = configparser.ConfigParser()
    config_path = path.expanduser("~/.better-twitter/config.ini")
    if path.exists(config_path):
        config.read(config_path)
    else:
        config["DEFAULT"]["consumer_key"] = input("Consumer Key: ")
        config["DEFAULT"]["consumer_secret"] = input("Consumer Secret: ")
        config["DEFAULT"]["access_token_key"] = input("Access Token Key: ")
        config["DEFAULT"]["access_token_secret"] = input("Access Token Secret: ")

        with open(config_path, "w") as config_file:
            config.write(config_file)

    api = twitter.Api(
        consumer_key=config["DEFAULT"]["consumer_key"],
        consumer_secret=config["DEFAULT"]["consumer_secret"],
        access_token_key=config["DEFAULT"]["access_token_key"],
        access_token_secret=config["DEFAULT"]["access_token_secret"]
    )
    return api


def parse():
    parser = argparse.ArgumentParser(
        description="Create a software license based on the given options")

    parser.add_argument(
        "--block-file", 
        action="store", 
        type=str, 
        required=False,
        help='Block multiple users from a file at once.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    
    api = load_api()
    args = parse()
    if args.block_file:
        block_from_file(api, args.block_file)
