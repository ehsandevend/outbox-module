from .base import IOutboxPublisher


class RedisPublisher(IOutboxPublisher):
    def publish(self, outbox):
        raise NotImplementedError()
