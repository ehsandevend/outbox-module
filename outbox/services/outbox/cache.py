from .base import IOutboxService


class CacheOutboxService(IOutboxService):
    def create_and_publish(self, instance, action):
        raise NotImplementedError()
