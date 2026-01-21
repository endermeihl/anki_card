"""将已有CSV中的collocations字段转换为HTML格式。"""

import csv
import re
from pathlib import Path


def convert_collocation_to_html(text: str) -> str:
    """将纯文本collocations转换为HTML格式。

    输入格式: "pattern → meaning; pattern2 → meaning2"
    输出格式: <div class="coll-item">...</div><div class="coll-item">...</div>
    """
    if not text or not text.strip():
        return ""

    # 用中英文分号分割
    items = re.split(r'[;；]', text)
    html_parts = []

    for item in items:
        item = item.strip()
        if not item:
            continue

        # 用箭头分割 pattern 和 meaning
        if '→' in item:
            parts = item.split('→', 1)
            pattern = parts[0].strip()
            meaning = parts[1].strip() if len(parts) > 1 else ""
        else:
            # 如果没有箭头，整个作为 pattern
            pattern = item
            meaning = ""

        html = f'<div class="coll-item"><span class="pattern">{pattern}</span>'
        if meaning:
            html += f'<span class="arrow">→</span><span class="meaning">{meaning}</span>'
        html += '</div>'
        html_parts.append(html)

    return ''.join(html_parts)


def process_csv(input_path: Path, output_path: Path = None):
    """处理CSV文件，转换collocations字段。"""
    if output_path is None:
        output_path = input_path

    rows = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 7:  # 确保有collocations字段（第7列，索引6）
                original = row[6]
                row[6] = convert_collocation_to_html(original)
            rows.append(row)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"已处理 {len(rows)} 行")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    csv_path = Path(__file__).parent.parent / "Anki_Auto_Builder" / "output" / "learning_import.csv"

    if csv_path.exists():
        process_csv(csv_path)
    else:
        print(f"文件不存在: {csv_path}")
