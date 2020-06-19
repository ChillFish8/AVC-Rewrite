

class BaseOption:
    def __init__(self, func, **kwargs):
        self._name = kwargs.pop('name', func.__name__)
        self._desc = kwargs.pop('description', func.__doc__)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.callback = func

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._desc

    def unload(self):
        return self.callback.__dict__


class OptionManager:
    options = {}

    @classmethod
    def get_option(cls, option_name):
        return cls.options.get(option_name)

    @classmethod
    def avc_option(cls, **kwargs):
        """ This is a deco that registers any options """
        def wrapper(func):
            wrapped = BaseOption(func, **kwargs)
            cls.options[wrapped.name] = wrapped
            return wrapped
        return wrapper

