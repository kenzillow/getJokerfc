#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import csv

# RFC IndexのXMLファイルのURL
url = 'https://www.rfc-editor.org/rfc-index.xml'

# XMLファイルをダウンロード
response = requests.get(url)

# ステータスコードを表示
print(f"HTTP Status Code: {response.status_code}")

# CSVファイルを書き込む準備
with open('rfc_list.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['RFC Number', 'Title', 'Date', 'Page Count', 'Current Status', 'Obsoleted By', 'Updated By'])

    # 成功した場合のみXMLを解析
    if response.status_code == 200:
        root = ET.fromstring(response.content)

        # 名前空間の定義
        ns = {'ns': 'http://www.rfc-editor.org/rfc-index'}

        # 名前空間を指定して各rfc-entry要素に対してループを行う
        for rfc_entry in root.findall('ns:rfc-entry', ns):
            date = rfc_entry.find('ns:date', ns)
            month = date.find('ns:month', ns).text
            day = date.find('ns:day', ns)

            # <day> が存在する場合のみテキストを取得
            day_text = day.text if day is not None else None

            # 作成日が4月1日であるかをチェック
            if month == 'April' and (day_text == '1' if day_text is not None else False):
                doc_id = rfc_entry.find('ns:doc-id', ns).text
                title = rfc_entry.find('ns:title', ns).text
                year = date.find('ns:year', ns).text
                date_str = f"{month} {day_text if day_text is not None else 'N/A'}, {year}"
                page_count = rfc_entry.find('ns:page-count', ns).text
                current_status = rfc_entry.find('ns:current-status', ns).text

                # obsoleted-byとupdated-byのdoc-idを取得
                obsoleted_by_ids = [e.text for e in rfc_entry.findall('ns:obsoleted-by/ns:doc-id', ns)]
                updated_by_ids = [e.text for e in rfc_entry.findall('ns:updated-by/ns:doc-id', ns)]

                # CSVに行を書き込む
                csv_writer.writerow([doc_id, title, date_str, page_count, current_status, ', '.join(obsoleted_by_ids), ', '.join(updated_by_ids)])

        print("CSV file has been created.")
    else:
        print("Failed to download the XML.")
