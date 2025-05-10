#!/usr/bin/env python3
import re
import sys
from collections import defaultdict

def find_duplicate_keys(path):
    # 字串檔裡 key 的正則
    key_pattern = re.compile(r'^\s*"(?P<key>[^"]+)"\s*=')
    occurrences = defaultdict(list)

    with open(path, encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            m = key_pattern.match(line)
            if m:
                key = m.group('key')
                occurrences[key].append(idx)

    # 篩選出重複的 key
    duplicates = {k: v for k, v in occurrences.items() if len(v) > 1}
    return duplicates

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/Localizable.strings", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    dup = find_duplicate_keys(path)
    if dup:
        print("發現重複的 key：")
        for key, lines in dup.items():
            print(f'  "{key}" 出現於行：{", ".join(map(str, lines))}')
        sys.exit(2)
    else:
        print("沒有發現重複的 key，全部獨一無二 👍")

if __name__ == "__main__":
    main()