from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from outbox.models import Outbox

from abc import ABC, abstractmethod


class IOutboxPublisher(ABC):

    @abstractmethod
    def publish(self, outbox: "Outbox"):
        raise NotImplementedError()
