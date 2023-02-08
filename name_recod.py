from app.media import Media
import os
import re
from zhon.hanzi import punctuation

os.environ["http_proxy"] = f"http://127.0.0.1:7890"
os.environ["https_proxy"] = f"http://127.0.0.1:7890"
os.environ["all_proxy"] = f"socks5://127.0.0.1:7890"

def exclude_cinese_sample(_text):
    unchinese = re.sub("[{}]".format(punctuation), "", _text)  # 排除中文符号

if __name__ == '__main__':
    file_name = r"/emby/D 斗罗大陆/S01E145.mp4"
    meds = Media().get_media_info_on_files([file_name,file_name])
    for med in list(meds.values()):
        print(med)
        for key, value in med.__dict__.items():
            print('{key}:{value}'.format(key=key, value=value))
