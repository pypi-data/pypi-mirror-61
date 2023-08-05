import ctypes
import json
import os
from logzero import logger

logger.debug("Loaded go generated SO library")

class KubernetesSelector():
    def __init__(self):
        lib_path = os.path.dirname(os.path.realpath(__file__))
        self.lib = ctypes.cdll.LoadLibrary(lib_path + '/libselector_wrapper.so')

    def match_label(self, selector, ls):
        ret = self.lib.match_label(ctypes.c_char_p(selector.encode('utf-8')),ctypes.c_char_p(json.dumps(ls).encode('utf-8')))
        return ret == 0

    def match_label_selector(self, labelsSelectorString, ls):
        ret = self.lib.match_label_selector(ctypes.c_char_p(json.dumps(labelsSelectorString).encode('utf-8')),ctypes.c_char_p(json.dumps(ls).encode('utf-8')))
        return ret == 0


