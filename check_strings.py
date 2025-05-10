#!/usr/bin/env python3
import re
import sys

def validate_strings_file(path):
    # 定義符合格式的正則：開頭 "..." = "..." ;
    pattern = re.compile(r'^\s*"[^"]+"\s*=\s*"[^"]+"\s*;\s*$')
    bad_lines = []

    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    visited = set()

    for idx, line in enumerate(lines):
        if idx in visited:
            continue
        # 跳過空行和註解
        if not line.strip() or line.strip().startswith("/*"):
            continue
        # 單行若符合格式，跳過
        if pattern.match(line):
            continue

        # 嘗試合併多行檢查（向下合併直到匹配或到達檔案末尾）
        merged = line.strip()
        merge_indices = [idx]
        success = False
        for j in range(idx + 1, len(lines)):
            # 跳過空行和註解行
            if not lines[j].strip() or lines[j].strip().startswith("/*"):
                continue
            merged += lines[j].strip()
            merge_indices.append(j)
            if pattern.match(merged):
                success = True
                break
            # 如果已經看到分號且仍不匹配，再繼續也不大可能符合，跳出
            if ";" in merged:
                break
        if success:
            # 標記這些行已經被成功合併檢查
            visited.update(merge_indices)
            continue

        # 若都無法符合格式，記錄此行
        bad_lines.append((idx+1, line.rstrip('\n')))

    return bad_lines

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/Localizable.strings", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    # 讀取原始檔案所有行
    with open(path, encoding='utf-8') as f:
        original_lines = f.readlines()

    bad = validate_strings_file(path)
    if bad:
        print("檢查到不符格式的行：")
        for ln, content in bad:
            print(f"  Line {ln}: {content}")
        sys.exit(2)
    else:
        print("全部都 OK 👍 格式都正確！")

if __name__ == "__main__":
    main()