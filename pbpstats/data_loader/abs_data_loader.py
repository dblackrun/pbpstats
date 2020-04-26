import abc


class AbsDataLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _load_data(self):
        pass

    @abc.abstractproperty
    def data(self):
        pass
