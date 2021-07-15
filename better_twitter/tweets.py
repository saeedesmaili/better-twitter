import time
import twitter
import pandas as pd
import pendulum as pn
from db import update_db


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