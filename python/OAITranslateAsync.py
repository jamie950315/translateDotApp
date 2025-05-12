import os
import pathlib
import asyncio
import re
import sys
from openai import AsyncOpenAI

client=AsyncOpenAI()
SCRIPT_DIR=pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR=SCRIPT_DIR/"Output"
APP_DIR=OUTPUT_DIR/(sys.argv[1])
UI_STRINGS_FILE=APP_DIR/"rawStrings"/"ui_strings.txt"
OUTPUT_FILE=APP_DIR/"zh-Hant.lproj"/"Localizable.strings"

MODEL="gpt-4.1-mini"
CHUNK_SIZE=100

ReceivedCount=0


with open(SCRIPT_DIR/"LLMTranslatePrompts.md", "r", encoding="utf-8") as f:
    instructions=f.read()

with open(UI_STRINGS_FILE, "r", encoding="utf-8") as f:
    all_strings=f.read().splitlines()



async def translate_chunk(chunk):

    prompt_input="\n".join(chunk)
    response=await client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=prompt_input
    )
    return response.output_text


async def translate_and_write(chunk, lock, chunkCount):

    global ReceivedCount
    translated=await translate_chunk(chunk)
    async with lock:
        ReceivedCount+=1
        print(f"[Translate] Received chunk: {ReceivedCount}/{chunkCount}")
        with open(OUTPUT_FILE, "a", encoding="utf-16") as out_fp:
            out_fp.write(translated)
            out_fp.write("\n")

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
        print("[Translate] Bad lines detected, automatically removing them...")
        bad_line_numbers={ln - 1 for ln, content in bad}
        filtered_lines=[line for idx, line in enumerate(original_lines) if idx not in bad_line_numbers]
        with open(OUTPUT_FILE, "w", encoding="utf-16") as f:
            f.writelines(filtered_lines)
        print("[Translate] Bad lines removed. All in the right format now.")
    else:
        print("[Translate] All in the right format")


async def main():
    with open(OUTPUT_FILE, "w", encoding="utf-16") as out_fp:
        out_fp.write("")

    lock=asyncio.Lock()
    tasks=[]

    if ((len(all_strings))%CHUNK_SIZE==0):
        chunkCount=(len(all_strings))//CHUNK_SIZE
    else:
        chunkCount=((len(all_strings))//CHUNK_SIZE)+1

    for i in range(0, len(all_strings), CHUNK_SIZE):
        chunk=all_strings[i : i+CHUNK_SIZE]
        tasks.append(asyncio.create_task(translate_and_write(chunk, lock, chunkCount)))
    
    print(f"[Translate] Dispatched chunk: {chunkCount}")
    print("[Translate] Waiting OpenAI API response...")
    await asyncio.gather(*tasks)
    ensure_format()
    print("[Translate] Complete")


if __name__ == "__main__":
    asyncio.run(main())