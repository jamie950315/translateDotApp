import os
import pathlib
import time
from openai import OpenAI

client=OpenAI()

PROJECT_DIR=pathlib.Path.home()/"Downloads"/"translating"

UI_STRINGS_FILE=PROJECT_DIR/"rawStrings"/"ui_strings.txt"
OUTPUT_FILE=PROJECT_DIR/"zh-Hant.lproj"/"Localizable.strings"

MODEL="gpt-4.1-mini"
CHUNK_SIZE=10
SLEEP_SEC=1


with open("LLMTranslatePrompts.md", "r", encoding="utf-8") as f:
    instructions=f.read()

with open(UI_STRINGS_FILE, "r", encoding="utf-8") as f:
    all_strings=f.read().splitlines()




def translate_chunk(chunk):

    prompt_input="\n".join(chunk)
    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=prompt_input
    )
    return response.output_text



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
            print("written")
            time.sleep(SLEEP_SEC)
            print("sleep 1 sec")


if __name__ == "__main__":
    main()