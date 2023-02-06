import os
import pickle
import random
import time
from threading import RLock

from app.config.config import Config
from app.utils import ExceptionUtils
from app.utils.commons import singleton

lock = RLock()

CACHE_EXPIRE_TIMESTAMP_STR = "cache_expire_timestamp"
EXPIRE_TIMESTAMP = 7 * 24 * 3600


@singleton
class MetaHelper(object):
    """
    {
        "id": '',
        "title": '',
        "year": '',
        "type": MediaType
    }
    """
    _meta_data = {}

    _meta_path = None
    _tmdb_cache_expire = False

    def __init__(self):
        self.init_config()

    def init_config(self):
        laboratory = Config().get_config('laboratory')
        if laboratory:
            self._tmdb_cache_expire = laboratory.get("tmdb_cache_expire")
        self._meta_path = os.path.join(Config().get_config_path(), 'tmdb.dat')
        self._meta_data = self.__load_meta_data(self._meta_path)

    def get_meta_data_by_key(self, key):
        """
        根据KEY值获取缓存值
        """
        with lock:
            info: dict = self._meta_data.get(key)
            if info:
                expire = info.get(CACHE_EXPIRE_TIMESTAMP_STR)
                if not expire or int(time.time()) < expire:
                    info[CACHE_EXPIRE_TIMESTAMP_STR] = int(time.time()) + EXPIRE_TIMESTAMP
                    self.update_meta_data({key: info})
                elif expire and self._tmdb_cache_expire:
                    self.delete_meta_data(key)
            return info or {}

    def delete_meta_data(self, key):
        """
        删除缓存信息
        @param key: 缓存key
        @return: 被删除的缓存内容
        """
        with lock:
            return self._meta_data.pop(key, None)

    @staticmethod
    def __load_meta_data(path):
        """
        从文件中加载缓存
        """
        try:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    data = pickle.load(f)
                return data
            return {}
        except Exception as e:
            ExceptionUtils.exception_traceback(e)
            return {}

    def update_meta_data(self, meta_data):
        """
        新增或更新缓存条目
        """
        if not meta_data:
            return
        with lock:
            for key, item in meta_data.items():
                if not self._meta_data.get(key):
                    item[CACHE_EXPIRE_TIMESTAMP_STR] = int(time.time()) + EXPIRE_TIMESTAMP
                    self._meta_data[key] = item

    def _random_sample(self, new_meta_data):
        """
        采样分析是否需要保存
        """
        ret = False
        if len(new_meta_data) < 25:
            keys = list(new_meta_data.keys())
            for k in keys:
                info = new_meta_data.get(k)
                expire = info.get(CACHE_EXPIRE_TIMESTAMP_STR)
                if not expire:
                    ret = True
                    info[CACHE_EXPIRE_TIMESTAMP_STR] = int(time.time()) + EXPIRE_TIMESTAMP
                elif int(time.time()) >= expire:
                    ret = True
                    if self._tmdb_cache_expire:
                        new_meta_data.pop(k)
        else:
            count = 0
            keys = random.sample(new_meta_data.keys(), 25)
            for k in keys:
                info = new_meta_data.get(k)
                expire = info.get(CACHE_EXPIRE_TIMESTAMP_STR)
                if not expire:
                    ret = True
                    info[CACHE_EXPIRE_TIMESTAMP_STR] = int(time.time()) + EXPIRE_TIMESTAMP
                elif int(time.time()) >= expire:
                    ret = True
                    if self._tmdb_cache_expire:
                        new_meta_data.pop(k)
                        count += 1
            if count >= 5:
                ret |= self._random_sample(new_meta_data)
        return ret
