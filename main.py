import json
import os
import re

levels_id = {
    "G3": 3,
    "G1": 1,
    "Conq": 0
}

tl_ranks = [
    "sssMonster",
    "ssMonster",
    "smonster",
    "amonster",
    "bmonster",
    "cmonster",
    "dmonster"
]

tl_tresholds = {
    "sssMonster": (8.0, 10),
    "ssMonster": (5.0, 7.9),
    "smonster": (4.0, 4.9),
    "amonster": (3.0, 3.9),
    "bmonster": (2.0, 2.9),
    "cmonster": (1.0, 1.9),
    "dmonster": (0.0, 0.9)
}

base_url = "https://m.swranking.com/api/monsterBase/getMonsterLevel"
mob_icon_base_url = "https://swarfarm.com/static/herders/images/monsters/"

raw_tl_folder_path = "tl_raw_data"  # folder containing the data "date_levelKey.json"
clean_tl_folder_path = "tl_clean_data"

date_list = [
    "2024-10-28",
    "2024-11-05",
    "2024-11-15",
    "2024-12-03",
    "2024-12-11",
    "2024-12-17",
    "2025-02-05"
]

# Get the data for each date
for date in date_list:
    for level in levels_id.keys():
        raw_filename = f"{raw_tl_folder_path}/{date}_{level}.json"

        with open(raw_filename, "r") as f:
            data = json.load(f)

        clean_data = []
        for rank in tl_ranks:
            for monster in data.get(rank, []):
                clean_data.append({
                    "monsterName": monster["monsterName"],
                    "monsterHeadImg": f"{mob_icon_base_url}{monster['monsterHeadImg']}",
                    "aiScore": monster["aiScore"]
                })

        clean_filename = f"{clean_tl_folder_path}/{date}_{level}.json"
        with open(clean_filename, "w") as f:
            json.dump(clean_data, f)

# Now create an aggregated tier list for each level
for level in levels_id.keys():
    files = [f for f in os.listdir(clean_tl_folder_path) if re.match(f".*_{level}.json", f)]

    data = []
    for file in files:
        with open(f"{clean_tl_folder_path}/{file}", "r") as f:
            data += json.load(f)

    monster_count = {}
    monster_images = {}
    for monster in data:
        name = monster["monsterName"]
        monster_count[name] = monster_count.get(name, 0) + 1
        monster_images[name] = monster["monsterHeadImg"]

    monster_score = {}
    for monster in data:
        if monster_count[monster["monsterName"]] >= 4:
            if monster["monsterName"] in monster_score:
                monster_score[monster["monsterName"]] += monster["aiScore"]
            else:
                monster_score[monster["monsterName"]] = monster["aiScore"]

    for monster in monster_score:
        monster_score[monster] /= monster_count[monster]

    tier_list = {}
    for monster in monster_score:
        for rank in tl_ranks:
            if tl_tresholds[rank][0] <= monster_score[monster] <= tl_tresholds[rank][1]:
                tier_list.setdefault(rank, []).append({
                    "monsterName": monster,
                    "monsterHeadImg": monster_images[monster],
                    "aiScore": monster_score[monster]
                })
                break

    with open(f"final_tierlists/{level}_tier_list.json", "w") as f:
        json.dump(tier_list, f, indent=4)

    print(f"Tier list for {level} created")
