from enum import Enum


class MediaType(Enum):
    TV = '电视剧'
    MOVIE = '电影'
    ANIME = '动漫'
    UNKNOWN = '未知'


class MatchMode(Enum):
    NORMAL = "正常模式"
    STRICT = "严格模式"


class OsType(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    SYNOLOGY = "Synology"
    MACOS = "MacOS"
    DOCKER = "Docker"
