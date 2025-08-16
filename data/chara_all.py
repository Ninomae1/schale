import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin, urlparse

# 設定
url = "https://bluearchive.wikiru.jp/?キャラクター一覧"
output_dir = "."
os.makedirs(output_dir, exist_ok=True)

# ページ取得
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

# テーブル取得
tables = soup.find_all("table", class_="style_table")

# 画像保存関数
def download_image(img_url, save_dir, filename_hint="image"):
    if isinstance(img_url, list):
        img_url = img_url[0]
    parsed = urlparse(img_url)
    ext = os.path.splitext(parsed.path)[1]
    if not ext:
        ext = ".png"
    filename = f"{filename_hint}{ext}"
    filepath = os.path.join(save_dir, filename)

    base, ext = os.path.splitext(filename)
    count = 1
    while os.path.exists(filepath):
        filename = f"{base}_{count}{ext}"
        filepath = os.path.join(save_dir, filename)
        count += 1

    try:
        response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filename
    except Exception as e:
        print(f"⚠ 画像取得失敗: {img_url} ({e})")
        return "[画像取得失敗]"

# テーブル処理
for idx, table in enumerate(tables, start=1):
    rows_raw = table.find_all("tr")
    if not rows_raw:
        continue

    rows = []

    for row_index, tr in enumerate(rows_raw):
        cells = tr.find_all(["th", "td"])
        row_data = []
        image_saved_in_row = False

        # ✅ キャラクター名は3列目（インデックス2）
        char_name = None
        if len(cells) > 2:
            char_name = cells[2].get_text(strip=True).replace("/", "_").replace("\\", "_")

        for cell in cells:
            img_tag = cell.find("img")
            if img_tag:
                img_src = img_tag.get("data-src") or img_tag.get("src")
                if isinstance(img_src, list):
                    img_src = img_src[0]
                if img_src and not img_src.startswith("data:"):
                    img_url = urljoin(url, img_src)

                    # ✅ スキップ対象テーブル
                    if idx in [35, 36, 37]:
                        row_data.append("[画像スキップ]")
                        continue

                    if idx == 38:
                        if not image_saved_in_row and char_name:
                            filename = download_image(img_url, output_dir, f"{char_name}_icon")
                            image_saved_in_row = True
                            row_data.append(filename)
                        else:
                            row_data.append("[画像スキップ]")
                    else:
                        filename = download_image(img_url, output_dir, f"table{idx}_row{row_index}")
                        row_data.append(filename)
                else:
                    row_data.append("[base64画像]")
            else:
                text = cell.get_text(strip=True)
                if "_icon.png" in text:
                    icon_url = f"https://bluearchive.wikiru.jp/?plugin=ref&page=キャラクター一覧&src={text}"

                    if idx in [35, 36, 37]:
                        row_data.append("[画像スキップ]")
                        continue

                    if idx == 38:
                        if not image_saved_in_row and char_name:
                            filename = download_image(icon_url, output_dir, f"{char_name}_icon")
                            image_saved_in_row = True
                            row_data.append(filename)
                        else:
                            row_data.append("[画像スキップ]")
                    else:
                        filename = download_image(icon_url, output_dir, text.replace("_icon.png", "") + "_icon")
                        row_data.append(filename)
                else:
                    row_data.append(text)
        if row_data:
            rows.append(row_data)

    if len(rows) < 2:
        continue

    headers = rows[0]
    data_rows = rows[1:]

    if idx == 38:
        csv_path = os.path.join(output_dir, "all_character.csv")
        with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data_rows)
        print(f"✅ テーブル[38] を保存: {csv_path}")
    else:
        print(f"\n--- [テーブル {idx}] 出力（先頭5行） ---")
        print(" | ".join(headers))
        for row in data_rows[:5]:
            print(" | ".join(row))
        print(f"...（全 {len(data_rows)} 行）\n")

print("🎉 完了：table38 キャラ画像（キャラ名_icon.png）保存済み、他も正常処理。")
