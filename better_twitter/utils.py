import time
import twitter
import pandas as pd
import pendulum as pn
from better_twitter import update_db



def block_from_file(api, con, file_path, df_accounts):
    df = pd.read_csv(file_path)
    if "user_id" not in df.columns:
        raise Exception("Couldn't find the user_id column in the file.")
    df["user_id"] = df["user_id"].astype(int)
    print(f"Blocking {df.shape[0]} users from file ...")
    for i, row in df.iterrows():
        if row["user_id"] in df_accounts["user_id"].values:
            print("already blocked")
            continue
        try:
            response = api.CreateBlock(user_id=row.user_id)
        except twitter.error.TwitterError as e:
            if e.message[0]["code"] == 50:  # User not found
                data = {
                    "user_id": row["user_id"],
                    "last_checked": str(pn.now()),
                    "comment": "User not found",
                }
                update_db(df, data, "accounts")
            elif e.message[0]["code"] == 88:  # rate limit
                print("API rate limit. Waiting for 5 minutes ...")
                time.sleep(300)
                pass
            else:
                raise Exception(e.message)

        data = {
            "user_id": row["user_id"],
            "screen_name": response.screen_name,
            "followers_count": response.followers_count,
            "followings_count": response.friends_count,
            "account_created_at": response.created_at,
            "last_checked": str(pn.now()),
        }
        update_db(df, data, "accounts")
        print(f"Blocked user: {row.screen_name}")