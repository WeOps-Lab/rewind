"""
i18n 国际化相关。该文件不要写任何业务代码，也不允许引入除系统外的模块
"""


class TranslateDict(dict):
    def __getitem__(self, item):
        value = super(TranslateDict, self).__getitem__(item)
        from django.utils.translation import gettext

        return gettext(value)

    def get(self, k, d=None):
        return self.__getitem__(k) if k in list(self.keys()) else d

    def copy(self):
        return TranslateDict(super(TranslateDict, self).copy())

    def items(self):
        return [(key, self.__getitem__(key)) for key in list(self.keys())]

    def values(self):
        return [self.__getitem__(key) for key in list(self.keys())]

    def iteritems(self):
        for k, v in super(TranslateDict, self).items():
            yield (k, self.__getitem__(k))
