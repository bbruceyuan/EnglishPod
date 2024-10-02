from jinja2 import Environment, FileSystemLoader
import os
import json
import math


def generate_html(title, dialogues, output_file, current_page_url):
    # 设置Jinja2环境
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./template.html')

    # 渲染模板
    output = template.render(title=title, dialogues=dialogues, current_page_url=current_page_url)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)


def process_content(content):
    dialogues = []
    lines = content.split('\n')
    current_speaker = None
    current_message = []

    for line in lines:
        if line.startswith('A:') or line.startswith('B:'):
            if current_speaker is not None:
                dialogues.append({
                    "speaker": current_speaker.lower(),
                    "message": ' '.join(current_message)
                })
            current_speaker = line[0]
            current_message = [line[3:].strip()]
        else:
            current_message.append(line.strip())

    if current_speaker is not None:
        dialogues.append({
            "speaker": current_speaker.lower(),
            "message": ' '.join(current_message)
        })

    return dialogues

def generate_html_for_all_items():
    # Read the JSON file
    with open('info.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    for item in items:
        number = item['number']
        name = item['name']
        content = item['content']

        title = f"{number} -- {name}"
        dialogues = process_content(content)
        url_slug = '-'.join(name.replace('-', ' ').split()).lower()
        output_file = f"./source/html/dialog/{number}-{url_slug}.html"
        current_page_url = f"/dialog/{number}-{url_slug}.html"

        generate_html(title, dialogues, output_file, current_page_url)
        print(f"HTML file generated: {output_file}")


def test():
    title = "001-English I love you!"
    dialogues = [
        {"speaker": "a", "message": "Has the game started yet? hello world, how can I help you? you should be a good boy how can I help you? you should be a good b how can I help you? you should be a good b", "timestamp": "2024/3/1 13:35:39"},
        {"speaker": "b", "message": "Yeah, about 5 minutes ago.", "timestamp": "2024/3/1 13:36:00"},
        # 添加更多对话...
    ]
    output_file = "./output.html"

    generate_html(title, dialogues, output_file)
    print(f"HTML file generated: {output_file}")


def generate_index_html(total_dialogs, group_size=20):
    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./index_template.html')

    # Read the JSON file to get dialog information
    with open('info.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    # Calculate number of groups
    num_groups = math.ceil(total_dialogs / group_size)

    # Generate dialog groups with URLs and titles
    dialog_groups = []
    for i in range(num_groups):
        start = i * group_size
        end = min((i + 1) * group_size, total_dialogs)
        dialogs = []
        for item in items[start:end]:
            number = item['number']
            name = item['name']
            url_slug = '-'.join(name.replace('-', ' ').split()).lower()
            dialog_url = f"/dialog/{number}-{url_slug}.html"
            dialog_title = f"{number} -- {name}"
            dialogs.append({
                'number': number,
                'url': dialog_url,
                'title': dialog_title
            })
        dialog_groups.append({
            'start': start + 1,
            'end': end,
            'dialogs': dialogs
        })

    # Render the template
    output = template.render(dialog_groups=dialog_groups)

    # Write the output to a file
    with open('./source/html/index.html', 'w', encoding='utf-8') as f:
        f.write(output)

# 示例用法
if __name__ == "__main__":
    # generate_html_for_all_items()
    generate_index_html(150)
