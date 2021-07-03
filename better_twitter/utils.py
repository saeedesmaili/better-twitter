import twitter
import pandas as pd


def block_from_file(api, file_path):
    df = pd.read_csv(file_path)
    if "user_id" not in df.columns:
        raise Exception("Couldn't find the user_id column in the file.")
    print(f"Blocking {df.shape[0]} users from file ...")
    for i, row in df.iterrows():
        try:
            api.CreateBlock(user_id=row.user_id)
            print(f"Blocked user: {row.screen_name}")
        except twitter.error.TwitterError as e:
            if e.message[0]["code"] == 50:  # User not found
                pass
            else:
                raise Exception(e.message)