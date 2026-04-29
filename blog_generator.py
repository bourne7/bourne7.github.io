import os
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
BASE_URL = 'https://github.com/bourne7/bourne7.github.io/blob/master/'
DEFAULT_CONTENT_DIRS = ('docs', '目录')
INDEX_MARKER = '<!-- 以上内容都是固定编辑的，下面的内容才会被python脚本替换 -->'


def resolve_content_root() -> Path:
    for candidate in DEFAULT_CONTENT_DIRS:
        path = REPO_ROOT / candidate
        if path.is_dir():
            return path
    raise FileNotFoundError(
        'No content directory found. Expected one of: ' + ', '.join(DEFAULT_CONTENT_DIRS)
    )


def format_display_name(name: str) -> str:
    original_name = name.capitalize()
    return uppercase_by_marker('_', original_name).replace('_', '')


def format_markdown_file(file_path: Path, content_root: Path) -> str:
    relative_path = file_path.relative_to(content_root.parent).as_posix()
    depth = len(file_path.relative_to(content_root).parts)
    indent = '  ' * max(depth - 1, 0)
    return f'{indent}* [{get_info_from_markdown(file_path)}]({BASE_URL}{relative_path})'


def render_directory(root_path: Path, content_root: Path) -> str:
    lines = []
    entries = sorted(root_path.iterdir(), key=lambda item: (item.is_file(), item.name.lower()))
    relative_parts = root_path.relative_to(content_root).parts

    if relative_parts:
        depth = len(relative_parts)
        directory_name = format_display_name(relative_parts[-1])
        if depth == 1:
            lines.append(f'### {directory_name}')
            lines.append('')
        else:
            indent = '  ' * (depth - 2)
            lines.append(f'{indent}* **{directory_name}**')
            lines.append('')

    for entry in entries:
        if entry.is_dir():
            rendered = render_directory(entry, content_root)
            if rendered:
                lines.append(rendered)
        elif entry.suffix.lower() == '.md':
            lines.append(format_markdown_file(entry, content_root))

    while lines and lines[-1] == '':
        lines.pop()
    return '\n'.join(lines)


# 根据标记将标记符号后面的字母变成大写。比如 Front_end_aaa -> Front_End_Aaa
def uppercase_by_marker(marker, original_string) -> str:
    for a in re.finditer(marker, original_string):
        position = a.span()[1]
        original_string = original_string[0:position] + \
            original_string[position:position + 1].upper() + \
            original_string[position + 1:]
    return original_string


def get_info_from_markdown(file_path: Path) -> str:
    with file_path.open('r', encoding='utf-8') as f:
        title = f.readline().replace('# ', '')
        date = f.readline().strip()
    # 如果匹配不上就给一个默认的显示
    if not re.search(r'^\d{4}-\d{2}-\d{2}$', date):
        date = ''
    else:
        date = ' (' + date + ')'
    # 读出来的每一行有个默认的换行符，这个和系统的换行符还没什么关系。所以只能选择全去掉
    return (title + date).replace('\r', '').replace('\n', '').replace('\r\n', '')


if __name__ == '__main__':
    index_path = REPO_ROOT / 'index.md'

    # 读取已有的文件
    with index_path.open('r', encoding='utf-8') as f:
        old_index = f.readlines()
    # file_index = open('index.md', 'r', encoding='utf-8')
    # old_index = file_index.readlines()

    # 将已有的index里面的前半部分内容挖出来
    new_index = ''
    for line in old_index:
        new_index += line
        # 这里需要一个分隔符，来区分不用改变的部分。
        if line.strip() == INDEX_MARKER:
            break

    if INDEX_MARKER not in ''.join(old_index):
        new_index = ''
        for line in old_index:
            if line.count('###') != 0:
                break
            new_index += line

    content_root = resolve_content_root()
    new_index += render_directory(content_root, content_root) + '\n'

    # 重新写入文件
    with index_path.open('w', encoding='utf-8') as f:
        f.write(new_index)
