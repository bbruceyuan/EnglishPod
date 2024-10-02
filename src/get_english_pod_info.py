import os
import re
import json

def get_english_pod_info():
    base_dir = 'EnglishPod'
    result = []

    for folder in sorted(os.listdir(base_dir)):
        match = re.match(r'(\d{3})', folder)
        if match:
            number = int(match.group(1))
            if 1 <= number <= 150:
                folder_path = os.path.join(base_dir, folder)
                if os.path.isdir(folder_path):
                    dialog_file = os.path.join(folder_path, 'dialog.txt')
                    if os.path.exists(dialog_file):
                        with open(dialog_file, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                        
                        # Extract the name from the MP4 file in the folder
                        name = ''
                        for file in os.listdir(folder_path):
                            if file.endswith('.mp4'):
                                name = os.path.splitext(file)[0]
                                break
                        
                        result.append({
                            'number': f'{number:03d}',
                            'name': name,
                            'content': content
                        })

    return result




if __name__ == '__main__':
    english_pod_info = get_english_pod_info()
    with open("info.json", "w", encoding="utf-8") as f:
        json.dump(english_pod_info, f, ensure_ascii=False)

