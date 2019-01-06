class HitLog(object):
    def __init__(self, value=None, **kwargs):
        if value:
            setattr(self, 'value', value)

        for k, v in kwargs.items():
            setattr(self, k, v)
      