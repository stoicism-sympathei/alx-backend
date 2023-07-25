#!/usr/bin/python3
""" Python caching systems """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO caching system """
    def __init__(self):
        """ Initialize class instance. """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key and item:
            self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded_key = sorted(self.cache_data)[0]
            self.cache_data.pop(discarded_key)
            print('DISCARD: {}'.format(discarded_key))

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key)
