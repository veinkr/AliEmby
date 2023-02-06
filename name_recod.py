from app.media import Media

if __name__ == '__main__':
    meds = Media().get_media_info_on_files(r"/home/vein/t16/play/emby/日韩剧/鱿鱼游戏 (2021)/Season 0/鱿鱼游戏 - S00E09 - 第9集.mkv")
    print(list(meds.values())[0])
    for med in list(meds.values()):
        for key, value in med.__dict__.items():
            print('{key}:{value}'.format(key=key, value=value))
