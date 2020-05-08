import abc


class Base(metaclass=abc.ABCMeta):
    """
    base class for all resources classes
    all resource classes should inherit from this
    """

    @abc.abstractproperty
    def data(self):
        pass
