# Generated with Gemini 3 Flash

from __future__ import annotations

import sys
import os
import chardet
from typing import Optional


def format_subtitles(input_text: str) -> str:
    # Split by double newlines to isolate each subtitle block
    blocks = input_text.strip().split('\n\n')
    formatted_blocks: list[str] = []

    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            formatted_blocks.append(block)
            continue
        
        header = lines[:2]     # Header: Index and Timestamp (first two lines)        
        content = lines[2:]    # Content: The actual subtitle text

        if len(content) > 2:
            # Join all lines except the last one into the first row
            # and keep the final line as the second row
            row1 = " ".join(content[:-1])
            row2 = content[-1]
            new_content = [row1, row2]
        else:
            new_content = content

        formatted_blocks.append("\n".join(header + new_content))

    return "\n\n".join(formatted_blocks)

def process_subtitle_file(file_path: str) -> tuple[str, Optional[str]]:
    try:
        # read, binary
        with open(file_path, 'rb') as file:
            raw_bytes = file.read()

        detected = chardet.detect(raw_bytes)
        encoding: Optional[str] = detected['encoding']

        if not encoding:
            print("Encoding was not detected, aborting")
            sys.exit(1)

        raw_content = raw_bytes.decode(encoding)
        formatted_text = format_subtitles(raw_content)

        return (formatted_text, encoding)

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    input_path = sys.argv[1]

    # Split name and extension, e.g. "old.srt" → "old" + ".srt"
    name, ext = os.path.splitext(input_path)
    output_path = f"{name}-new{ext}"  # → "old-new.srt"
    result, encoding = process_subtitle_file(input_path)

    with open(output_path, 'w', encoding=encoding) as f:
        f.write(result)
        
    print(f"Saved to: {output_path}")
