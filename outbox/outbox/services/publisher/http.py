import requests
from django.conf import settings

from outbox.services.publisher.base import IOutboxPublisher


class SingleHTTPPublisher(IOutboxPublisher):

    def __init__(self):
        self.url = settings.outbox["OUTBOX"]["HTTP_PUBLISHER"]["NO_SQL_WRAPPER"]["SINGLE"]

    def publish(self, outbox):
        try:
            response = requests.post(self.url, json=outbox.payload, timeout=10)
            response.raise_for_status()
            outbox.mark_as_delivered()
            return True
        except Exception as e:
            outbox.mark_as_failed(str(e))
            return False


class BulkHTTPPublisher(IOutboxPublisher):
    def __init__(self):
        self.url = settings.outbox["OUTBOX"]["HTTP_PUBLISHER"]["NO_SQL_WRAPPER"]["BULK"]

    def publish(self, outbox):
        try:
            response = requests.post(self.url, json=outbox.payload, timeout=10)
            response.raise_for_status()
            outbox.mark_as_delivered()
            return True
        except Exception as e:
            outbox.mark_as_failed(str(e))
            return False
