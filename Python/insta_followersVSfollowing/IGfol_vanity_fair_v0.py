import pandas as pd
import json

def load_instagram_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle different root structures
    if isinstance(data, dict):
        # If it has relationships_following, use that list
        if "relationships_following" in data:
            data = data["relationships_following"]
        else:
            # If it's a dict but with another key, raise an error for debugging
            raise ValueError(f"Unexpected JSON structure in {file_path}")

    records = []
    for entry in data:
        for s in entry.get("string_list_data", []):
            records.append({
                "value":s.get("value"),
                "timestamp": s.get("timestamp")
            })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["timestamp"], unit ="s")
    return df

def find_nonfollowers(followers_file, following_file, output_csv):
    df_followers = load_instagram_json(followers_file)
    df_following = load_instagram_json(following_file)

    followers_set = set(df_followers["value"].str.lower())
    following_set = set(df_following["value"].str.lower())

    not_following_back = following_set - followers_set

    df_result = pd.DataFrame({"instahandle":sorted(not_following_back)})
    df_result.to_csv(output_csv, index=False, sep=";", encoding="utf-8")
    print(f"Done! {len(df_result)} non-followers found out of {len(df_following)}")


followers_file = "D:/Downloads/connections/followers_and_following/followers_1.json"
following_file = "D:/Downloads/connections/followers_and_following/following.json"
output_csv = "D:/Downloads/connections/followers_and_following/non_followers.csv"

find_nonfollowers(followers_file, following_file, output_csv)