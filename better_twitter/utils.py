import twitter
import pandas as pd
import pendulum as pn


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
            df_accounts = df_accounts.append({
                "user_id": row["user_id"],
                "screen_name": response.screen_name,
                "followers_count": response.followers_count,
                "followings_count": response.friends_count,
                "account_created_at": response.created_at,
                "last_checked": str(pn.now()),                
            }, ignore_index=True)
            df_accounts.to_sql("accounts", con=con, index=False, if_exists="replace")
            print(f"Blocked user: {row.screen_name}")
        except twitter.error.TwitterError as e:
            if e.message[0]["code"] == 50:  # User not found
                pass
            else:
                raise Exception(e.message)