import os
import shutil
import re
import shutil

SRC_DIR = "notebooks_src"
DEST_DIR = "content/notebooks"

CN_NUM = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

def cn2an(text):
    if not text: return 0
    if text.isdigit(): return int(text)
    val = 0
    if text.startswith('十'):
        if len(text) == 1: return 10
        if len(text) == 2 and text[1] in CN_NUM: return 10 + CN_NUM[text[1]]
    if '十' in text:
        parts = text.split('十')
        if parts[0] in CN_NUM: val += CN_NUM[parts[0]] * 10
        if len(parts) > 1 and parts[1] in CN_NUM: val += CN_NUM[parts[1]]
        return val
    if text in CN_NUM: return CN_NUM[text]
    return 0

def parse_weight(name):
    match = re.search(r'第([0-9零一二三四五六七八九十]+)[篇章部节讲]', name)
    if match:
        num_str = match.group(1)
        val = cn2an(num_str)
        if val > 0: return val * 10

    match = re.match(r'^(\d+)', name)
    if match: return int(match.group(1)) * 10

    return 999

def clean_title(name):
    """提取干净标题：只去掉纯数字排序前缀 (1. xxx)，绝对保留中文编号 (第一篇 xxx)"""
    # 之前这里有一行代码删除了中文编号，现已移除，确保保留 "第一篇" 等前缀

    # 仅移除 "1. ", "01_", "1- " 等纯数字排序前缀
    # 逻辑：数字开头 + 可选的分隔符(., -, _) + 空格
    name = re.sub(r'^[0-9]+[\.\-_]?\s*', '', name)

    # 替换下划线为空格
    name = name.replace('_', ' ')
    return name.strip()

def process_file(file_path, weight, title):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        if not lines or lines[0].strip() != "---":
            new_lines = [
                "---\n",
                f"title: \"{title}\"\n",
                f"weight: {weight}\n",
                "---\n"
            ] + lines
        else:
            new_lines = []
            dash_count = 0
            inserted = False
            has_title = False

            for line in lines:
                if line.strip().startswith("title:"):
                    has_title = True
                    # 如果原文件没有标题（不太可能），或者标题是文件名，可以考虑覆盖
                    # 但为了安全，我们不覆盖已有的 title，只注入 weight
                    pass
                if line.strip() == "---":
                    dash_count += 1

                # 在第二个 --- 之前插入
                if dash_count == 2 and not inserted and line.strip() == "---":
                    if not has_title:
                        new_lines.append(f"title: \"{title}\"\n")
                    new_lines.append(f"weight: {weight}\n")
                    inserted = True

                new_lines.append(line)

        with open(file_path, "w") as f:
            f.writelines(new_lines)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def create_index(dir_path, title, weight, collapse=True, extra_content=""):
    index_path = os.path.join(dir_path, "_index.md")

    with open(index_path, "w") as f:
        f.write("---\n")
        f.write(f"title: \"{title}\"\n")
        f.write(f"weight: {weight}\n")
        if collapse:
            f.write("bookCollapseSection: true\n")
        f.write("---\n")
        if extra_content:
            f.write(extra_content)

def build_content():
    if not os.path.exists(SRC_DIR):
        print(f"Error: {SRC_DIR} does not exist.")
        return

    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)

    print(f"Copying {SRC_DIR} -> {DEST_DIR}...")
    shutil.copytree(SRC_DIR, DEST_DIR, ignore=shutil.ignore_patterns('.git', '.github'))

    print("Processing weights and indices...")
    for root, dirs, files in os.walk(DEST_DIR):
        dirs.sort()

        # 1. 寻找并处理 README
        readme_content = ""
        readme_file = None
        for filename in files:
            if filename.lower() == "readme.md":
                readme_file = filename
                break

        if readme_file:
            path = os.path.join(root, readme_file)
            try:
                with open(path, 'r') as f:
                    content = f.read()
                    # 去掉 front matter
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            content = parts[2]

                    if content.strip():
                        readme_content = "\n\n" + content

                os.remove(path)
                print(f"Merged README for: {root}")
            except Exception as e:
                print(f"Error merging README: {e}")

        # 2. 生成 _index.md
        rel_path = os.path.relpath(root, DEST_DIR)
        dirname = os.path.basename(root)

        if rel_path == ".":
            create_index(root, "首页", 10, collapse=False, extra_content=readme_content)
        else:
            weight = parse_weight(dirname)
            if weight == 999: weight = 9999
            create_index(root, dirname, weight, extra_content=readme_content)

        # 3. 处理普通笔记
        for filename in files:
            if filename == readme_file or filename == "_index.md" or not filename.endswith(".md"):
                continue

            name_no_ext = os.path.splitext(filename)[0]
            weight = parse_weight(name_no_ext)
            if weight == 999: weight = 9999

            clean_name = clean_title(name_no_ext)
            process_file(os.path.join(root, filename), weight, clean_name)

    print("Build complete!")

if __name__ == "__main__":
    build_content()
