#!/usr/bin/env python3
import re
import sys
import pathlib


def validate_strings_file(path):
    pattern = re.compile(r'^\s*"[^"]+"\s*=\s*"[^"]+"\s*;\s*$')
    bad_lines = []

    with open(path, encoding='utf-16') as f:
        lines = f.readlines()

    visited = set()

    for idx, line in enumerate(lines):
        if idx in visited:
            continue
        if not line.strip() or line.strip().startswith("/*"):
            continue
        if pattern.match(line):
            continue

        merged = line.strip()
        merge_indices = [idx]
        success = False
        for j in range(idx + 1, len(lines)):
            if not lines[j].strip() or lines[j].strip().startswith("/*"):
                continue
            merged += lines[j].strip()
            merge_indices.append(j)
            if pattern.match(merged):
                success = True
                break
            if ";" in merged:
                break
        if success:
            visited.update(merge_indices)
            continue

        bad_lines.append((idx+1, line.rstrip('\n')))

    return bad_lines

def main():

    path=pathlib.Path.home()/"Downloads"/"translating"/"zh-Hant.lproj"/"Localizable.strings"
    with open(path, encoding='utf-16') as f:
        original_lines = f.readlines()

    bad = validate_strings_file(path)
    if bad:
        print("Lines in wrong format")
        for ln, content in bad:
            print(f"  Line {ln}: {content}")
        sys.exit(2)
    else:
        print("All in the right format")

if __name__ == "__main__":
    main()