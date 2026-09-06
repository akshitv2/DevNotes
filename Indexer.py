import os
import re

def generate_index(root_dir, output_file="INDEXD.md"):
    index_lines = ["# Directory Index\n\n"]
    
    for dirpath, _, filenames in sorted(os.walk(root_dir)):
        md_files = [f for f in sorted(filenames) if f.endswith(".md") and f != output_file]
        if not md_files:
            continue
            
        rel_path = os.path.relpath(dirpath, root_dir)
        indent_level = 0 if rel_path == "." else rel_path.count(os.sep) + 1
        indent = "  " * indent_level
        
        if rel_path != ".":
            index_lines.append(f"{'  ' * (indent_level - 1)}* **{os.path.basename(dirpath)}/**\n")
            
        for file in md_files:
            file_path = os.path.join(dirpath, file)
            title = file
            
            # Extract first H1 header for title if available
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"^#\s+(.+)", line.strip())
                    if match:
                        title = match.group(1)
                        break
                        
            rel_file_path = os.path.relpath(file_path, root_dir).replace("\\", "/")
            index_lines.append(f"{indent}* [{title}]({rel_file_path})\n")

    with open(os.path.join(root_dir, output_file), "w", encoding="utf-8") as f:
        f.writelines(index_lines)

# Usage: Run in the directory containing your folders/md files
generate_index(".")