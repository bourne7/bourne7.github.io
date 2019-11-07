import json
import os
import re


# 深度优先遍历所有的文件
def get_all_files(root_path, file_dict):
    for dir_file in os.listdir(root_path):
        # 这里要处理一下路径，原因是传到下一级的时候也需要只保持最右边的目录级别。
        path_elements = root_path.split(os.sep)
        root_dir_key_name = path_elements[path_elements.__len__() - 1]

        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)

        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            if root_dir_key_name not in file_dict.keys():
                file_dict[root_dir_key_name] = {}
            file_dict[root_dir_key_name][dir_file] = {}
            get_all_files(dir_file_path, file_dict[root_dir_key_name])

        # 判断该路径为文件还是路径
        if os.path.isfile(dir_file_path):
            file_ext = os.path.splitext(dir_file)[1][1:]
            if not file_ext == 'md':
                continue
            if root_dir_key_name not in file_dict.keys():
                file_dict[root_dir_key_name] = {}
            file_dict[root_dir_key_name][dir_file] = file_ext


# 扁平化一棵树，将内容输出到文本
def flat_tree(root_path, file_dict, flat_content):
    for key in file_dict:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, key)
        # 将文件添加到扁平化的数据里面去
        flat_content = flat_content + markdown_formatter(dir_file_path) + '\n'
        # 如果是个目录，就递归里面的内容
        if os.path.isdir(dir_file_path):
            flat_content = flat_tree(dir_file_path, file_dict[key], flat_content)
    return flat_content


# 根据层级的不同，将不同的内容格式化成为不同的内容。
def markdown_formatter(content_string):
    sep_count = content_string.count(os.sep)
    if sep_count == 0:
        # 这里是包含了所有文章的根目录
        content_string = '## ' + content_string
    elif sep_count == 1:
        # 这里是一级目录，比如 技术 和 生活 分类
        content_string = '\n' + '### ' + content_string.split(os.sep)[1] + '\n'
    elif sep_count == 2:
        # 这里是二级目录，比如 java，git 等等
        original_name = content_string.split(os.sep)[2].capitalize()
        content_string = '* **' + uppercaseByMarker('_', original_name).replace('_', '') + '**'
    elif sep_count == 3:
        # 内容文章需要提供一个基础连接。
        base_url = 'https://github.com/bourne7/bourne7.github.io/blob/master/'
        # 文章的连接
        content_string = '  * [' + get_info_from_markdown(content_string) + '](' + base_url + content_string + ')'
        # 替换 反斜杠到正斜杠
        content_string = content_string.replace('\\', '/')
    return content_string


# 根据标记将标记符号后面的字母变成大写。比如 Front_end_aaa -> Front_End_Aaa
def uppercaseByMarker(marker, original_string):
    for a in re.finditer(marker, original_string):
        position = a.span()[1]
        original_string = original_string[0:position] + \
                          original_string[position:position + 1].upper() + \
                          original_string[position + 1:]
    return original_string


def get_info_from_markdown(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        title = f.readline().replace('# ', '')
        date = f.readline()
    # 如果匹配不上就给一个默认的显示
    if not re.search(r'^\d{4}-\d{2}-\d{2}$', date):
        date = ''
    else:
        date = ' (' + date + ')'
    # 读出来的每一行有个默认的换行符，这个和系统的换行符还没什么关系。所以只能选择全去掉
    return (title + date).replace('\r', '').replace('\n', '').replace('\r\n', '')


if __name__ == '__main__':
    # 文章所在的文件夹
    article = '目录'

    # 读取已有的文件
    with open('index.md', 'r', encoding='utf-8') as f:
        old_index = f.readlines()
    # file_index = open('index.md', 'r', encoding='utf-8')
    # old_index = file_index.readlines()

    # 将已有的index里面的前半部分内容挖出来
    new_index = ''
    for line in old_index:
        if line.count(article) != 0:
            break
        new_index += line

    # 读取所有的 markdown 目录
    file_dict = {}
    get_all_files(article, file_dict)
    content = json.dumps(file_dict, indent=2, ensure_ascii=False)

    # 深度优先遍历一下所有的 markdown
    flat_content = ''
    new_index += flat_tree(r'', file_dict, flat_content)
    print(new_index)

    # 重新写入文件
    with open('index.md', 'w', encoding='utf-8') as f:
        f.write(new_index)
