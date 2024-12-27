import os
import re
from bs4 import BeautifulSoup

def extract_video_paths(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        video_paths = set()
        for source_tag in soup.find_all('source'):
            src = source_tag.get('src')
            if src and src.startswith('./videos/'):
                video_paths.add(src.lstrip('./'))
            if src and src.startswith('videos/'):
                video_paths.add(src.lstrip('./'))
        return video_paths

def list_all_files(directory):
    all_files = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            all_files.add(relative_path)
    return all_files

def delete_unused_files(directory, used_files):
    all_files = set([os.path.join('videos', i) for i in list_all_files(directory)])
    unused_files = all_files - used_files
    for file in unused_files:
        file_path = file
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

# 主函数
def main():
    html_file = 'index.html'
    videos_directory = 'videos'

    used_video_paths = extract_video_paths(html_file)
    print("Used video paths:")
    for path in used_video_paths:
        print(path)

    delete_unused_files(videos_directory, used_video_paths)

if __name__ == "__main__":
    main()