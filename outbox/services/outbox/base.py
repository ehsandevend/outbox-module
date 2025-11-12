from abc import ABC, abstractmethod
from outbox.shared.enums import ActionChoices


class IOutboxService(ABC):

    @abstractmethod
    def create_and_publish(self, instance, action: ActionChoices) -> bool:
        pass
