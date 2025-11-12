from outbox.repository import OutboxRepo
from outbox.services.publisher.http import (
    SingleSaveHTTPPublisher,
    SingleUpdateHTTPPublisher,
    BulkHTTPPublisher,
)
from outbox.shared.enums import ActionChoices
from .base import IOutboxService

class SingleSaveOutboxService(IOutboxService):
    def __init__(self):
        self.repo = OutboxRepo()
        self.publisher = SingleSaveHTTPPublisher()

    def create_and_publish(self, instance, action=ActionChoices.CREATE) -> bool:
        outbox_obj = self.repo.create_single_log_outbox(instance, action)
        return self.publisher.publish(outbox_obj)

class SingleUpdateOutboxService(IOutboxService):
    def __init__(self):
        self.repo = OutboxRepo()
        self.publisher = SingleUpdateHTTPPublisher()

    def create_and_publish(self, instance, action=ActionChoices.CREATE) -> bool:
        outbox_obj = self.repo.create_single_log_outbox(instance, action)
        return self.publisher.publish(outbox_obj)

class BulkLogOutboxService(IOutboxService):
    def __init__(self):
        self.repo = OutboxRepo()
        self.publisher = BulkHTTPPublisher()

    def create_and_publish(self, instances, action=ActionChoices.CREATE) -> bool:
        outbox_obj = self.repo.create_bulk_log_outbox(instances, action)
        return self.publisher.publish(outbox_obj)
