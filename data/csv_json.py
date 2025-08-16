import csv
import json
import os

input_csv = "character/all_character.csv"
output_json = "character/characters.json"

characters = []

with open(input_csv, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    
    # 1行目をヘッダーとして取得（これが列名）
    header_row = next(reader)

    # それ以降がデータ行（空白や不完全な行はスキップ）
    data_rows = [row for row in reader if any(cell.strip() for cell in row)]

    # 装備の列はheader_rowから「装備」で始まるものを抽出
    equip_columns = [(i, col) for i, col in enumerate(header_row) if "装備" in col]

    for row in data_rows:
        # 空行や長さの合わない行はスキップ
        if len(row) != len(header_row):
            continue

        row_dict = dict(zip(header_row, row))

        # 「名前」列は「名前」でなくて「名前」の前に「名前」列ある？
        # 今回のヘッダーは「名前」なのでそれで取得
        name = row_dict.get("名前", "").strip()
        if not name:
            continue

        # レア度は最初に「★3」のようにあるが「★」を取り除いて数字だけ取得
        raw_rarity = row_dict.get("レア", "").strip()
        rarity = 1
        if raw_rarity.startswith("★"):
            try:
                rarity = int(raw_rarity[1:])
            except:
                pass

        school = row_dict.get("学校", "不明").strip()

        equipment = []
        for idx, label in equip_columns:
            equip_name = row[idx].strip() if idx < len(row) else ""
            equipment.append({
                "name": equip_name,
                "currentLevel": 1,
                "targetLevel": 1
            })

        char_data = {
            "name": name,
            "school": school,
            "rarity": rarity,
            "iconPath": f"assets/icons/{name}_icon.png",
            "currentLevel": 1,
            "targetLevel": 1,
            "skills": [
                {"name": "EXスキル", "currentLevel": 1, "targetLevel": 1},
                {"name": "ノーマルスキル", "currentLevel": 1, "targetLevel": 1},
                {"name": "パッシブスキル", "currentLevel": 1, "targetLevel": 1},
                {"name": "サブスキル", "currentLevel": 1, "targetLevel": 1}
            ],
            "weapon": [
                {
                    "name": "固有武器",
                    "type": row_dict.get("武器種", "").strip(),
                    "weaponRelease": 1,
                    "currentLevel": 1,
                    "targetLevel": 1
                }
            ],
            "equipment": equipment,
            "mysticRelease": {
                "current": rarity,
                "target": rarity
            }
        }

        characters.append(char_data)

# 保存
os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(characters, f, ensure_ascii=False, indent=2)

print(f"✅ JSONファイルを保存しました: {output_json}")
