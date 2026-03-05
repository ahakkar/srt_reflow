# Generated with Gemini 3 Flash

import re
import sys
import os

def format_subtitles(input_text):
    # Split by double newlines to isolate each subtitle block
    blocks = input_text.strip().split('\n\n')
    formatted_blocks = []

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

def process_subtitle_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            raw_content = file.read()
        
        formatted_text = format_subtitles(raw_content)        

        return formatted_text

    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    input_path = sys.argv[1]

    # Split name and extension, e.g. "old.srt" → "old" + ".srt"
    name, ext = os.path.splitext(input_path)
    output_path = f"{name}-new{ext}"  # → "old-new.srt"
    result = process_subtitle_file(input_path)

    with open(output_path, 'w', encoding='utf-8-sig') as f:
        f.write(result)
        
    print(f"Saved to: {output_path}")
