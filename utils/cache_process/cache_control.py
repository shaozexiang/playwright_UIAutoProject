# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : cache_control.py
"""
"""
获取缓存数据并写入缓存数据
这里需要扩展使用redis进行实际的数据存储
"""
cache_data = {}


class CacheHandler:
    class_cache = {}
    func_cache = {}

    @classmethod
    def set_funcCache(cls, key, value):
        cls.func_cache[key] = value

    @classmethod
    def clear_funcCache(cls):
        cls.func_cache.clear()

    @classmethod
    def get_funcCache(cls, key):
        if key in cls.func_cache.keys():
            return cls.func_cache.get(key)
        else:
            raise KeyError(
                f"获取缓存出错，未找到需要获取的缓存值"
                f"缓存的的键为{key}"
            )

    @classmethod
    def set_clsCache(cls, key, value):
        cls.class_cache[key] = value

    @classmethod
    def clear_clsCache(cls):
        cls.class_cache.clear()

    @classmethod
    def get_clsCache(cls, key):
        if key in cls.class_cache.keys():
            return cls.class_cache.get(key)
        else:
            raise KeyError(
                f"获取缓存出错，未找到需要获取的缓存值"
                f"缓存的的键为{key}"
            )

    @classmethod
    def get_cache(cls, cache_key):
        if cache_key in cache_data.keys():
            return cache_data.get(cache_key)
        else:
            raise KeyError(
                f"获取缓存出错，未找到需要获取的缓存值"
                f"缓存的的键为{cache_key}"
            )

    @classmethod
    def update_cache(cls, cache_key, cache_value):
        cache_data[cache_key] = cache_value

    @classmethod
    def clear_cache(cls, key):
        cache_data[key] = None


