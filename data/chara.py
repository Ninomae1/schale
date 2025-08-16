import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import quote
import ntpath  # ファイル名だけ取る用

CHARACTER_DIR = os.path.join("character", "chara")
ALL_CHARACTER_CSV = os.path.join(CHARACTER_DIR, "all_character.csv")
BASE_URL = "https://bluearchive.wikiru.jp/?"

def sanitize_filename(name):
    # 英数字と、スペース・ハイフン・アンダースコア・半角括弧・全角括弧を許可
    allowed_chars = " _-()（）"
    return "".join(c if c.isalnum() or c in allowed_chars else "_" for c in name)

def get_detail_page_html(char_name):
    url = BASE_URL + quote(char_name)
    print(f"Fetching {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    return response.text

def parse_character_details(html):
    soup = BeautifulSoup(html, "html.parser")
    tds = soup.find_all("td", valign="top")
    results = []

    for td in tds:
        # 画像があれば title を取得
        imgs = td.find_all("img")
        for img in imgs:
            title = img.get("title")
            if title:
                results.append(f"[画像タイトル: {title}]")

        # テキストも含めて取得
        text = td.get_text("\n", strip=True)
        if text:
            results.append(text)

    return results

def save_character_csv(char_name, details_list):
    os.makedirs(CHARACTER_DIR, exist_ok=True)
    filename = sanitize_filename(char_name) + ".csv"
    path = os.path.join(CHARACTER_DIR, filename)

    print(f"Saving to filename: {filename}")  # デバッグ用：ファイル名確認

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for detail in details_list:
            writer.writerow([detail])
    print(f"Saved details for {char_name} -> {path}")

def main():
    if not os.path.exists(ALL_CHARACTER_CSV):
        print(f"Error: {ALL_CHARACTER_CSV} が見つかりません。先にall_character.csvを用意してください。")
        return

    with open(ALL_CHARACTER_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            char_name = row.get("名前")
            if not char_name:
                continue

            html = get_detail_page_html(char_name)
            details = parse_character_details(html)
            if details:
                save_character_csv(char_name, details)
            else:
                print(f"⚠ {char_name} の詳細データが見つかりませんでした。")

if __name__ == "__main__":
    main()
