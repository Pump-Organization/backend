import abc


class AbstractEventHandler(abc.ABC):
    def __init__(self, event):
        self._event = event

    @abc.abstractmethod
    def process(self, event):
        pass
