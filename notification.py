from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def notify(self, message: str):
        self._strategy.send_notification(message)
