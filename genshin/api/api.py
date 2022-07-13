import abc

from genshin.models import GenshinUserData

'''
对外提供数据的api
'''

# API 提供对外接口


class API(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def index(self, uid: int) -> GenshinUserData:
        pass
