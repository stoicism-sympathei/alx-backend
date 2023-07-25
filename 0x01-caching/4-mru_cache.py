#!/usr/bin/python3
""" Python caching systems """
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """ MRU caching system
    """
    def __init__(self):
        """ Initialize class instance. """
        super().__init__()
        self.cache_data = OrderedDict()
        self.mru = ""

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if key in self.cache_data:
                    self.cache_data.update({key: item})
                    self.mru = key
                else:
                    # discard the most recently used item
                    discarded = self.mru
                    del self.cache_data[discarded]
                    print("DISCARD: {}".format(discarded))
                    self.cache_data[key] = item
                    self.mru = key
            else:
                self.cache_data[key] = item
                self.mru = key

    def get(self, key):
        """ Get an item by key
        """
        if key in self.cache_data:
            self.mru = key
            return self.cache_data[key]
