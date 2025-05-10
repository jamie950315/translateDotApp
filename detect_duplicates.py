#!/usr/bin/env python3
import re
import sys
from collections import defaultdict

def find_duplicate_keys(path):
    key_pattern = re.compile(r'^\s*"(?P<key>[^"]+)"\s*=')
    occurrences = defaultdict(list)

    with open(path, encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            m = key_pattern.match(line)
            if m:
                key = m.group('key')
                occurrences[key].append(idx)

    duplicates = {k: v for k, v in occurrences.items() if len(v) > 1}
    return duplicates

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/Localizable.strings", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    dup = find_duplicate_keys(path)
    if dup:
        print("Found repeat key:")
        for key, lines in dup.items():
            print(f'  "{key}" appear in Line:{", ".join(map(str, lines))}')
        sys.exit(2)
    else:
        print("No repeat key found, all unique 👍")

if __name__ == "__main__":
    main()