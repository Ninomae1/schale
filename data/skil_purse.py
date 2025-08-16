from pathlib import Path
import csv
import re

# キャラCSVの読み込みと処理
def process_csv(file_path, output_dir):
    with open(file_path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    def find_skill_name(keyword):
        indexes = [i for i, line in enumerate(lines) if line == keyword]
        for idx in indexes:
            if idx + 1 < len(lines) and lines[idx + 1] == "†":
                for offset in range(2, 10):
                    if idx + offset < len(lines):
                        candidate = lines[idx + offset].strip()
                        if candidate and not candidate.startswith("Lv"):
                            return candidate
        return "不明"

    # スキル名の抽出
    ex_skill_name = find_skill_name("EXスキル")
    normal_skill_name = find_skill_name("ノーマルスキル")
    passive_skill_name = find_skill_name("パッシブスキル")
    sub_skill_name = find_skill_name("サブスキル")

    # 素材名の取得（24〜37行目, 40〜62行目） ※0-indexed
    raw_material_names = lines[23:37] + lines[39:62]
    material_names = [re.sub(r"\[画像タイトル:\s*|\]", "", name).strip() for name in raw_material_names]

    # x数字の抽出（最初の2つはスキップ）
    x_matches_all = re.findall(r"x(\d+)", "\n".join(lines))
    x_matches = x_matches_all[2:]  # 最初の2個を無視

    # 数と素材名の対応付け（素材数よりx数が多い場合は無視）
    material_map = []
    for name, count in zip(material_names, x_matches):
        material_map.append(f"{name}: {count}")

    # キャラ名取得
    char_name = Path(file_path).stem.replace("_成長素材", "")

    # 出力ディレクトリ作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # 出力ファイル名
    output_path = output_dir / f"{char_name}_skill.csv"

    # CSV 出力
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["EXスキル"])
        writer.writerow([ex_skill_name])
        writer.writerow(["2"])
        writer.writerow(material_map[0:2])
        writer.writerow(["3"])
        writer.writerow(material_map[2:6])
        writer.writerow(["4"])
        writer.writerow(material_map[6:10])
        writer.writerow(["5"])
        writer.writerow(material_map[10:14])
        writer.writerow(["ノーマルスキル"])
        writer.writerow([normal_skill_name])
        writer.writerow(["パッシブスキル"])
        writer.writerow([passive_skill_name])
        writer.writerow(["サブスキル"])
        writer.writerow([sub_skill_name])
        writer.writerow(["2"])
        writer.writerow(material_map[14:15])
        writer.writerow(["3"])
        writer.writerow(material_map[15:16])
        writer.writerow(["4"])
        writer.writerow(material_map[16:19])
        writer.writerow(["5"])
        writer.writerow(material_map[19:22])
        writer.writerow(["6"])
        writer.writerow(material_map[22:25])
        writer.writerow(["7"])
        writer.writerow(material_map[25:28])
        writer.writerow(["8"])
        writer.writerow(material_map[28:32])
        writer.writerow(["9"])
        writer.writerow(material_map[32:36])  # ← 4つに修正
        writer.writerow(["10"])
        writer.writerow(material_map[36:37])

    print(f"完了: {output_path.name}")
    return output_path.name

# 実行: character フォルダ内のすべてのCSVファイルを処理
character_dir = Path("character/chara")
output_dir = character_dir / "skill"

for csv_file in character_dir.glob("*.csv"):
    process_csv(csv_file, output_dir)
