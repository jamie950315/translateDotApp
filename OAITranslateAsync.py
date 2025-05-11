import os
import pathlib
import asyncio
from openai import AsyncOpenAI

client=AsyncOpenAI()

PROJECT_DIR=pathlib.Path.home()/"Downloads"/"translating"

UI_STRINGS_FILE=PROJECT_DIR/"rawStrings"/"ui_strings.txt"
OUTPUT_FILE=PROJECT_DIR/"zh-Hant.lproj"/"Localizable.strings"

MODEL="gpt-4.1-mini"
CHUNK_SIZE=10


with open("LLMTranslatePrompts.md", "r", encoding="utf-8") as f:
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


async def translate_and_write(chunk, lock):
    translated=await translate_chunk(chunk)
    async with lock:
        with open(OUTPUT_FILE, "a", encoding="utf-16") as out_fp:
            out_fp.write(translated)
            out_fp.write("\n")


async def main():
    with open(OUTPUT_FILE, "w", encoding="utf-16") as out_fp:
            out_fp.write("")

    lock=asyncio.Lock()
    tasks=[]
    for i in range(0, len(all_strings), CHUNK_SIZE):
        chunk=all_strings[i : i + CHUNK_SIZE]
        print("dispatching chunk")
        tasks.append(asyncio.create_task(translate_and_write(chunk, lock)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())