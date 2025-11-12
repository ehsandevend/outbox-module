import requests
from django.conf import settings

from outbox.services.publisher.base import IOutboxPublisher


class SingleSaveHTTPPublisher(IOutboxPublisher):

    def __init__(self):
        self.url = settings.OUTBOX["OUTBOX"]["HTTP_PUBLISHER"]["NO_SQL_WRAPPER"]["SINGLE"]["CREATE"]

    def publish(self, outbox):
        try:
            response = requests.post(self.url, json=outbox.payload, timeout=10)
            response.raise_for_status()
            outbox.mark_as_delivered()
            return True
        except Exception as e:
            outbox.mark_as_failed(str(e))
            return False
        
class SingleUpdateHTTPPublisher(IOutboxPublisher):

    def __init__(self):
        self.url = settings.OUTBOX["OUTBOX"]["HTTP_PUBLISHER"]["NO_SQL_WRAPPER"]["SINGLE"]["UPDATE"]

    def publish(self, outbox):
        try:
            response = requests.patch(f"{self.url}{outbox.payload['id']}", json=outbox.payload, timeout=10)
            response.raise_for_status()
            outbox.mark_as_delivered()
            return True
        except Exception as e:
            outbox.mark_as_failed(str(e))
            return False


class BulkHTTPPublisher(IOutboxPublisher):
    def __init__(self):
        self.url = settings.OUTBOX["OUTBOX"]["HTTP_PUBLISHER"]["NO_SQL_WRAPPER"]["BULK"]

    def publish(self, outbox):
        try:
            response = requests.post(self.url, json=outbox.payload, timeout=10)
            response.raise_for_status()
            outbox.mark_as_delivered()
            return True
        except Exception as e:
            outbox.mark_as_failed(str(e))
            return False
