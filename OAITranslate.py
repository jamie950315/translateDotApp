import os
import pathlib
import time
import re
import sys
from openai import OpenAI

client=OpenAI()

PROJECT_DIR=pathlib.Path.home()/"Downloads"/"translating"

UI_STRINGS_FILE=PROJECT_DIR/"rawStrings"/"ui_strings.txt"
OUTPUT_FILE=PROJECT_DIR/"zh-Hant.lproj"/"Localizable.strings"

MODEL="gpt-4.1-mini"
CHUNK_SIZE=500
SLEEP_SEC=1


with open("LLMTranslatePrompts.md", "r", encoding="utf-8") as f:
    instructions=f.read()

with open(UI_STRINGS_FILE, "r", encoding="utf-8") as f:
    all_strings=f.read().splitlines()




def translate_chunk(chunk):

    prompt_input="\n".join(chunk)
    response=client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=prompt_input
    )
    return response.output_text


def validate_strings_file():

    pattern=re.compile(r'^\s*"[^"]+"\s*=\s*"[^"]+"\s*;\s*$')
    bad_lines=[]

    with open(OUTPUT_FILE, encoding='utf-16') as f:
        lines=f.readlines()

    visited=set()

    for idx, line in enumerate(lines):
        if idx in visited:
            continue
        if not line.strip() or line.strip().startswith("/*"):
            continue
        if pattern.match(line):
            continue

        merged=line.strip()
        merge_indices=[idx]
        success=False
        for j in range(idx + 1, len(lines)):
            if not lines[j].strip() or lines[j].strip().startswith("/*"):
                continue
            merged+=lines[j].strip()
            merge_indices.append(j)
            if pattern.match(merged):
                success=True
                break
            if ";" in merged:
                break
        if success:
            visited.update(merge_indices)
            continue

        bad_lines.append((idx+1, line.rstrip('\n')))

    return bad_lines

def ensure_format():

    with open(OUTPUT_FILE, encoding='utf-16') as f:
        original_lines=f.readlines()

    bad=validate_strings_file()
    if bad:
        print("Bad lines detected, automatically removing them...")
        bad_line_numbers={ln - 1 for ln, content in bad}
        filtered_lines=[line for idx, line in enumerate(original_lines) if idx not in bad_line_numbers]
        with open(OUTPUT_FILE, "w", encoding="utf-16") as f:
            f.writelines(filtered_lines)
        print("Bad lines removed. All in the right format now.")
    else:
        print("All in the right format")


def main():

    with open(OUTPUT_FILE, "w", encoding="utf-16") as out_fp:
        for i in range(0, len(all_strings), CHUNK_SIZE):
            chunk=all_strings[i : i + CHUNK_SIZE]
            print("translating")
            translated=translate_chunk(chunk)
            print("translated")
            out_fp.write(translated)
            out_fp.write("\n")
            out_fp.flush()
            time.sleep(SLEEP_SEC)
            print("chunk complete")

    ensure_format()
    print("Complete")


if __name__ == "__main__":
    main()