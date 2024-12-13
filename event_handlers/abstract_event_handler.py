import abc


class AbstractEventHandler(abc.ABC):
    @abc.abstractmethod
    def process(self, event):
        pass
